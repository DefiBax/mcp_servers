from mcp.server.fastmcp import FastMCP, Context
from mcp.shared.exceptions import McpError
from mcp.types import ErrorData, INTERNAL_ERROR, INVALID_PARAMS
import logging
import time
from voice_recorder.audio_service import AudioService
from .config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create an MCP server
mcp = FastMCP("VoiceRecorder")

# Initialize the audio service
config = get_config()
audio_service = AudioService(model_name=config.whisper_model)


@mcp.tool()
def start_recording() -> str:
    """Start recording audio from the default microphone"""
    try:
        return audio_service.start_recording()
    except Exception as e:
        logger.error(f"Error starting recording: {str(e)}")
        raise McpError(ErrorData(INTERNAL_ERROR, f"Recording error: {str(e)}"))


@mcp.tool()
def stop_and_transcribe() -> str:
    """Stop recording and transcribe the audio to text"""
    try:
        audio_data, msg = audio_service.stop_recording()
        if audio_data is None:
            return msg

        return audio_service.transcribe(audio_data)
    except Exception as e:
        logger.error(f"Error during transcription: {str(e)}")
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

        # Start recording
        start_recording()
        logger.info(f"Recording for {duration_seconds} seconds")

        # Wait for specified duration
        time.sleep(duration_seconds)

        # Stop and transcribe
        return stop_and_transcribe()
    except Exception as e:
        logger.error(f"Error in record_and_transcribe: {str(e)}")
        # Make sure recording is stopped in case of error
        if audio_service.is_recording:
            try:
                audio_service.stop_recording()
            except:
                pass
        raise McpError(ErrorData(INTERNAL_ERROR, f"Error: {str(e)}"))