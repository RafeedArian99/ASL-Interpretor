import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

class AudioRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Recorder App")

        # Variable to track recording state
        self.recording = False

        # Record Button
        self.record_button = tk.Button(root, text="Record", command=self.toggle_record)
        self.record_button.pack(pady=10)

        # Text Display
        self.text_display = tk.Text(root, height=5, width=50)
        self.text_display.pack(pady=10)

        # Matplotlib Panel
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot_panel = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Initialize animation
        self.anim = None
        self.frames = []  # list of frames, each frame is a list of 2D points
        self.init_animation()

    def toggle_record(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.recording = True
        self.record_button.config(text="Recording...")
        # Replace this with your actual recording functionality
        self.text_display.delete(1.0, tk.END)
        self.text_display.update()


    def stop_recording(self):
        self.recording = False
        self.record_button.config(text="Record")
        # Replace this with your actual recording functionality
        # self.text_display.insert(tk.END, "Recording stopped.\n")
        self.text_display.update()


    def init_animation(self):
        # Initialize the animation
        self.anim = animation.FuncAnimation(self.figure, self.update_plot, frames=len(self.frames), interval=200, repeat=True)

    def update_plot(self, frame):
        self.plot_panel.clear()
        # Draw points and edges for the current frame
        points = self.frames[frame]
        if points:
            self.plot_panel.scatter(*zip(*points))
        self.plot_panel.set_title('Frame {}'.format(frame))
        self.plot_panel.set_xlabel('X')
        self.plot_panel.set_ylabel('Y')
        self.plot_panel.set_xlim(0, 256)  # Set your desired limits
        self.plot_panel.set_ylim(0, 256)  # Set your desired limits
        self.plot_panel.grid(True)

# Sample frames
frames = [
    [(1, 1), (2, 2), (3, 3)],
    [(2, 2), (3, 3), (4, 4)],
    [(3, 3), (4, 4), (5, 5)]
]

# Create root window
root = tk.Tk()

# Create the app
app = AudioRecorderApp(root)
app.frames = frames  # Assign frames to the app

# Start the Tkinter event loop
root.mainloop()
