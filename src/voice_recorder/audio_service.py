import time
import threading
import numpy as np
import sounddevice as sd
from queue import Queue
import whisper
import logging

logger = logging.getLogger(__name__)


class AudioService:
    def __init__(self, model_name="base.en", sample_rate=16000):
        """Initialize the audio service with recording and transcription capabilities"""
        self.is_recording = False
        self.sample_rate = sample_rate
        self.stop_event = None
        self.data_queue = None
        self.recording_thread = None

        # Initialize transcriber
        logger.info(f"Loading Whisper model: {model_name}")
        try:
            self.transcriber = whisper.load_model(model_name)
            logger.info(f"Whisper model '{model_name}' loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {str(e)}")
            raise

    def start_recording(self):
        """Start recording audio from the default microphone"""
        if self.is_recording:
            return "Already recording"

        self.data_queue = Queue()
        self.stop_event = threading.Event()

        def callback(indata, frames, time, status):
            if status:
                logger.warning(f"Recording status: {status}")
            self.data_queue.put(bytes(indata))

        def record_thread():
            try:
                with sd.RawInputStream(
                        samplerate=self.sample_rate,
                        dtype="int16",
                        channels=1,
                        callback=callback
                ):
                    logger.info("Recording started")
                    while not self.stop_event.is_set():
                        time.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in recording thread: {str(e)}")

        self.recording_thread = threading.Thread(target=record_thread)
        self.recording_thread.daemon = True  # Make thread exit when main program exits
        self.recording_thread.start()
        self.is_recording = True

        return "Recording started"

    def stop_recording(self):
        """Stop recording and return the audio data"""
        if not self.is_recording:
            return None, "Not recording"

        self.stop_event.set()
        self.recording_thread.join()
        self.is_recording = False

        logger.info("Processing audio data...")
        audio_data = b"".join(list(self.data_queue.queue))
        audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

        return audio_np, "Recording stopped"

    def transcribe(self, audio_np):
        """Transcribe audio data to text"""
        if audio_np is None or audio_np.size == 0:
            return "No audio recorded"

        logger.info("Transcribing audio...")
        try:
            result = self.transcriber.transcribe(audio_np, fp16=False)
            transcription = result["text"].strip()
            logger.info(f"Transcription completed: {transcription[:30]}...")
            return transcription
        except Exception as e:
            logger.error(f"Error during transcription: {str(e)}")
            raise