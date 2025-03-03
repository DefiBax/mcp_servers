from .config import get_config
from .server import mcp, audio_service

def main():
    """Voice Recorder MCP: Record audio and transcribe using Whisper."""
    # Config is automatically loaded when server is imported
    mcp.run()

__all__ = ["mcp", "audio_service", "main"]