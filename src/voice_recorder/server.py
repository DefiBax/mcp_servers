from mcp.server.fastmcp import FastMCP, Context
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
import time
import threading
import numpy as np
import sounddevice as sd
from queue import Queue
import sys
import whisper

# Initialize main components
# Use global variables to maintain state across calls
is_recording = False
recording_thread = None
stop_event = None
data_queue = None
transcriber = None

# Create an MCP server
mcp = FastMCP("VoiceRecorder")


def initialize_transcriber(model_name="base.en"):
    """Initialize the transcriber with the specified model"""
    global transcriber
    try:
        # Print diagnostic information to stderr, not stdout
        print(f"Loading Whisper model: {model_name}", file=sys.stderr)
        transcriber = whisper.load_model(model_name)
        return transcriber
    except Exception as e:
        print(f"Error loading Whisper model: {str(e)}", file=sys.stderr)
        raise


def record_audio(stop_event, data_queue):
    """
    Capture audio data from the microphone and add it to a queue
    """

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        data_queue.put(bytes(indata))

    try:
        with sd.RawInputStream(
                samplerate=16000, dtype="int16", channels=1, callback=callback
        ):
            print("Recording started", file=sys.stderr)
            while not stop_event.is_set():
                time.sleep(0.1)
    except Exception as e:
        print(f"Error in recording thread: {str(e)}", file=sys.stderr)


@mcp.tool()
def start_recording() -> str:
    """Start recording audio from the default microphone"""
    global is_recording, recording_thread, stop_event, data_queue

    try:
        if is_recording:
            return "Already recording"

        data_queue = Queue()
        stop_event = threading.Event()
        recording_thread = threading.Thread(
            target=record_audio,
            args=(stop_event, data_queue),
        )
        recording_thread.start()
        is_recording = True
        return "Recording started"
    except Exception as e:
        print(f"Error starting recording: {str(e)}", file=sys.stderr)
        raise McpError(ErrorData(INTERNAL_ERROR, f"Recording error: {str(e)}"))


@mcp.tool()
def stop_and_transcribe() -> str:
    """Stop recording and transcribe the audio to text"""
    global is_recording, recording_thread, stop_event, data_queue, transcriber

    try:
        if not is_recording:
            return "Not recording"

        if transcriber is None:
            initialize_transcriber()

        stop_event.set()
        recording_thread.join()
        is_recording = False

        print("Processing audio data...", file=sys.stderr)
        audio_data = b"".join(list(data_queue.queue))
        audio_np = (
                np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
        )

        if audio_np.size == 0:
            return "No audio recorded"

        # Transcribe the audio
        print("Transcribing audio...", file=sys.stderr)
        result = transcriber.transcribe(audio_np, fp16=False)
        transcription = result["text"].strip()
        print(f"Transcription completed: {transcription}", file=sys.stderr)
        return transcription
    except Exception as e:
        print(f"Error during transcription: {str(e)}", file=sys.stderr)
        if is_recording:
            try:
                stop_event.set()
                recording_thread.join()
                is_recording = False
            except:
                pass
        raise McpError(ErrorData(INTERNAL_ERROR, f"Transcription error: {str(e)}"))


@mcp.tool()
def record_and_transcribe(duration_seconds: int) -> str:
    """
    Record audio for the specified duration and transcribe it

    Args:
        duration_seconds: Number of seconds to record (1-60)
    """
    try:
        # Validate input
        if not isinstance(duration_seconds, int) or duration_seconds < 1 or duration_seconds > 60:
            raise McpError(
                ErrorData(INVALID_PARAMS, "Duration must be between 1 and 60 seconds")
            )

        if transcriber is None:
            initialize_transcriber()

        # Start recording
        result = start_recording()
        print(f"Started recording for {duration_seconds} seconds", file=sys.stderr)

        # Wait for specified duration
        time.sleep(duration_seconds)

        # Stop and transcribe
        return stop_and_transcribe()
    except ValueError as e:
        print(f"Parameter error: {str(e)}", file=sys.stderr)
        raise McpError(ErrorData(INVALID_PARAMS, str(e)))
    except Exception as e:
        print(f"Unexpected error: {str(e)}", file=sys.stderr)
        raise McpError(ErrorData(INTERNAL_ERROR, f"Unexpected error: {str(e)}"))


# # Add prompts for common use cases
# @mcp.prompt()
# def transcribe_speech() -> str:
#     return """Please transcribe what I say next. I'll start speaking after you acknowledge this request."""
#
#
# @mcp.prompt()
# def meeting_notes() -> str:
#     return """I'd like to record meeting notes. Please let me speak, and then organize what I say into clear, structured meeting notes with action items."""
#
#
# @mcp.prompt()
# def summarize_recording() -> str:
#     return """I'd like to record something and have you summarize it. Let me know when you're ready for me to start speaking."""


# Initialize transcriber with default model when imported
initialize_transcriber()