import assemblyai as aai

aai.settings.api_key = "6d511fc2ce154a959683cbbc782c1bc1"


class Transcriber:
    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        print("Session ID:", session_opened.session_id)

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            print(transcript.text, end="\n")
            self.queue.put(transcript.text)
            remaining = "\n".join(self.queue.queue)
            self.text_panel.delete(1.0, "end")
            self.text_panel.insert("end", remaining)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        print("An error occured:", error)

    def on_close(self):
        print("Closing Session")

    def __init__(self, queue, text_panel) -> None:
        self.queue = queue
        self.text_panel = text_panel
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16_000,
            on_data=self.on_data,
            on_error=self.on_error,
            on_open=self.on_open,
            on_close=self.on_close,
        )
        self.microphone_stream = None

    def start(self):
        self.transcriber.connect()

        self.microphone_stream = aai.extras.MicrophoneStream(sample_rate=16_000)
        self.transcriber.stream(self.microphone_stream)

    def close(self):
        self.transcriber.close()
