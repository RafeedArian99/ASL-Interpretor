import sys
from queue import Queue
import tkinter as tk
from threading import Thread
import re
import numpy as np

from transcriber import Transcriber
from landmark_reader import WordReader, MESHDATA, WORDDATA
from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class TranscriptionApp:
    def __init__(self):
        self.llm = OpenAI(temperature=0.8)
        self.pose_colors = {"face": "blue", "pose": "green", "rhand": "red", "lhand": "orange"}

        self.root = tk.Tk()
        self.root.configure(bg="white")

        self.text_panel = tk.Text(self.root, height=5)
        self.text_panel.pack()

        self.canvas = tk.Canvas(self.root, width=512, height=512, bg="white")
        self.canvas.pack()

        self.queue = Queue()

        self.transcriber = Transcriber(self.queue, self.text_panel)
        self.transcription_thread = Thread(target=self.transcriber.start)
        self.transcription_thread.start()

        self.processing_thread = Thread(target=self.translate_sentences)
        self.processing_thread_flag = True
        self.processing_thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def play_animation(self, word):
        wr = WordReader(word)
        pose_color_items = self.pose_colors.items()

        for frame in range(wr.num_frames):
            self.canvas.delete(tk.ALL)
            self.canvas.create_text(256, 15, text=word, fill="black", font=("", 30))
            for pose, color in pose_color_items:
                for [i, j] in MESHDATA[pose[-4:]]:
                    self.canvas.create_line(
                        *wr.get(pose, frame, i, 2), *wr.get(pose, frame, j, 2), fill=color
                    )
            self.canvas.after(30)

        wr.close()

    def play_transition(self, last_word, cur_word):
        lw = WordReader(last_word)
        last_frame = []
        for pose in self.pose_colors:
            for i in range(lw.info[pose][1]):
                last_frame.append(lw.get(pose, lw.num_frames - 1, i, 2))
        last_frame = np.array(last_frame)

        cw = WordReader(cur_word)
        cur_frame = []
        for pose in self.pose_colors:
            for i in range(cw.info[pose][1]):
                cur_frame.append(cw.get(pose, 0, i, 2))
        cur_frame = np.array(cur_frame)

        transition = [last_frame]
        for i in np.linspace(0, 1, 15):
            intp = (1 - i) * last_frame + i * cur_frame
            transition.append(intp)
        transition.append(cur_frame)

        pose_color_items = self.pose_colors.items()
        for frame in transition:
            self.canvas.delete(tk.ALL)
            for pose, color in pose_color_items:
                pose_strt, pose_end = lw.info[pose]
                pose_end += pose_strt
                for [i, j] in MESHDATA[pose[-4:]]:
                    self.canvas.create_line(
                        *frame[pose_strt:pose_end][i],
                        *frame[pose_strt:pose_end][j],
                        fill=color,
                    )
            self.canvas.after(30)

        lw.close()
        cw.close()

    def process_translation(self, translation):
        words = re.split(r"[^a-zA-Z0-9]", translation)
        ret_words = [w.lower() for w in words if w and not w.isspace()]
        words = [w.lower() for w in words if w and not w.isspace()]
        for i, w in enumerate(words):
            w = w.lower()
            if w in WORDDATA:
                w = f"\033[32m{w}\033[0m"
            else:
                w = "".join(("\033[33m" if c in WORDDATA else "\033[31m") + c for c in w)
                w += "\033[0m"
            words[i] = w

        print(" ".join(words))
        return ret_words

    def translate_sentences(self):
        last_word = None
        while self.processing_thread_flag:
            l = self.queue.get()
            translation = self.llm.invoke(
                "If there was an English-to-ASL translator that took in a sentence as input, "
                + "and outputed the words (not signs) in proper ASL order, how would it translate "
                + f'the phrase "{l}"? Provide only the output of this translator and nothing else.'
            )

            words = self.process_translation(translation)
            for w in words:
                if last_word:
                    self.play_transition(last_word, w)
                if w in WORDDATA:
                    self.play_animation(w)
                    last_word = w
                else:
                    for c in w:
                        if c in WORDDATA:
                            self.play_animation(c)
                            last_word = c

            remaining = "\n".join(self.queue.queue)
            self.text_panel.delete(1.0, "end")
            self.text_panel.insert("end", remaining)

            self.queue.task_done()

    def run(self):
        self.root.mainloop()

    def close(self):
        self.transcriber.close()
        self.root.destroy()
        self.processing_thread_flag = False
        self.processing_thread.join()
        sys.exit()


if __name__ == "__main__":
    app = TranscriptionApp()
    app.run()
