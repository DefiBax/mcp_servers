import time
import threading
import numpy as np
import sounddevice as sd
from queue import Queue

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.stop_event = None
        self.data_queue = None
        self.recording_thread = None
        
    def record_audio(self, stop_event, data_queue):
        """
        Captures audio data from the user's microphone and adds it to a queue for further processing.
        
        Args:
            stop_event (threading.Event): An event that, when set, signals the function to stop recording.
            data_queue (queue.Queue): A queue to which the recorded audio data will be added.
        """
        def callback(indata, frames, time, status):
            if status:
                print(status)
            data_queue.put(bytes(indata))

        with sd.RawInputStream(
            samplerate=16000, dtype="int16", channels=1, callback=callback
        ):
            while not stop_event.is_set():
                time.sleep(0.1)
                
    def start_recording(self):
        """Start recording audio"""
        if self.is_recording:
            return "Already recording"
        
        self.data_queue = Queue()
        self.stop_event = threading.Event()
        self.recording_thread = threading.Thread(
            target=self.record_audio,
            args=(self.stop_event, self.data_queue),
        )
        self.recording_thread.start()
        self.is_recording = True
        return "Recording started"
        
    def stop_recording(self):
        """Stop recording audio and return the recorded data"""
        if not self.is_recording:
            return None, "Not recording"
            
        self.stop_event.set()
        self.recording_thread.join()
        self.is_recording = False
        
        audio_data = b"".join(list(self.data_queue.queue))
        audio_np = (
            np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        )
        
        return audio_np, "Recording stopped"
