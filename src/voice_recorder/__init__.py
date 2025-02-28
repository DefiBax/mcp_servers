import argparse
from .server import mcp

def main():
    """Voice Recorder MCP: Record audio and transcribe using Whisper."""
    parser = argparse.ArgumentParser(
        description="MCP server for voice recording and transcription using Whisper."
    )
    parser.add_argument('--model', default='base.en', help='Whisper model to use')
    args = parser.parse_args()
    
    # Initialize the transcriber with the specified model
    from .server import initialize_transcriber
    initialize_transcriber(args.model)
    
    # Run the MCP server
    mcp.run()

if __name__ == "__main__":
    main()
