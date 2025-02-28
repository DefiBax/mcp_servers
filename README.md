# Voice Recorder MCP Server

An MCP server for recording audio and transcribing it using OpenAI's Whisper model. Designed to work as a Goose custom extension.

## Features

- Record audio from the default microphone
- Transcribe recordings using Whisper
- Integrates with Goose AI agent as a custom extension
- Includes prompts for common recording scenarios

## Installation

### Using Conda

```bash
# Clone the repository
git clone https://github.com/yourusername/voice-recorder-mcp.git
cd voice-recorder-mcp

# Create and activate the conda environment
conda env create -f environment.yml
conda activate voice-recorder-mcp

# Install the package
pip install -e .

## Usage

### As a Standalone MCP Server

```bash
# Run as a CLI tool
voice-recorder-mcp

# Use a specific Whisper model
voice-recorder-mcp --model medium.en
```

### Testing with MCP Inspector

```bash
# permission run.sh
chmod +x run.sh
```

```bash
# Run in development mode
./run.sh
```

### Preparing for Goose AI Agent

```bash
# Find absolute path
which voice-recorder-mcp
```

```bash
# Sync UV
uv sync
```

### With Goose AI Agent

1. Open Goose and go to Settings > Extensions > Add > Command Line Extension
2. Set the name to `voice-recorder`
3. In the Command field, enter:
   ```
   uv run /full/path/to/voice-recorder-mcp/.venv/bin/voice-recorder-mcp
   ```
   Or for a specific model:
   ```
   uv run /full/path/to/voice-recorder-mcp/.venv/bin/voice-recorder-mcp --model medium.en
   ```
4. Do not add environment variables
5. When you run a new session you need to tell the session to take action off your transcription OR you can tell goose
to add to global memories "I want you to take action from transcriptions returned by voice-recorder. For example if I tell you 1+1 you return
the result. If you are unsure, you can ask me for clarification"
## Available Tools

- `start_recording`: Start recording audio from the default microphone
- `stop_and_transcribe`: Stop recording and transcribe the audio to text
- `record_and_transcribe`: Record audio for a specified duration and transcribe it

## Available Prompts (NOT USABLE YET WIP)

- `transcribe_speech`: Basic transcription request
- `meeting_notes`: Record and organize meeting notes
- `summarize_recording`: Record and summarize content

## Whisper Models

This extension supports various Whisper model sizes:

- `tiny.en`: Fastest, lowest accuracy (good for testing)
- `base.en`: Fast with decent accuracy (default)
- `small.en`: Good balance of speed and accuracy
- `medium.en`: High accuracy but slower
- `large`: Highest accuracy but much slower and resource-intensive

## Requirements

- Python 3.10+
- An audio input device (microphone)
- Internet connection (for initial model download)

## Troubleshooting

### Common Issues

- **No audio being recorded**: Check your microphone permissions and settings
- **Model download errors**: Ensure you have a stable internet connection for the initial model download
- **Integration with Goose**: Make sure the command path is correct and permissions are set properly

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
