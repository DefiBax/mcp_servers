# Voice Recorder MCP Server

An MCP server for recording audio and transcribing it using OpenAI's Whisper model. Designed to work as a Goose custom extension or standalone MCP server.

## Features

- Record audio from the default microphone
- Transcribe recordings using Whisper
- Integrates with Goose AI agent as a custom extension
- Includes prompts for common recording scenarios

## Installation

```bash
# Install from source
git clone https://github.com/DefiBax/voice-recorder-mcp.git
cd voice-recorder-mcp
pip install -e .
```

## Usage

### As a Standalone MCP Server

```bash
# Run with default settings (base.en model)
voice-recorder-mcp

# Use a specific Whisper model
voice-recorder-mcp --model medium.en

# Adjust sample rate
voice-recorder-mcp --sample-rate 44100
```

### Testing with MCP Inspector

The MCP Inspector provides an interactive interface to test your server:

```bash
# Install the MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Run your server with the inspector
npx @modelcontextprotocol/inspector voice-recorder-mcp
```

### With Goose AI Agent

1. Open Goose and go to Settings > Extensions > Add > Command Line Extension
2. Set the name to `voice-recorder`
3. In the Command field, enter the full path to the voice-recorder-mcp executable:
   ```
   /full/path/to/voice-recorder-mcp
   ```
   
   Or for a specific model:
   ```
   /full/path/to/voice-recorder-mcp --model medium.en
   ```
   
   To find the path, run:
   ```bash
   which voice-recorder-mcp
   ```

4. No environment variables are needed for basic functionality
5. Start a conversation with Goose and introduce the recorder with:
   "I want you to take action from transcriptions returned by voice-recorder. For example, if I dictate a calculation like 1+1, please return the result."

## Available Tools

- `start_recording`: Start recording audio from the default microphone
- `stop_and_transcribe`: Stop recording and transcribe the audio to text
- `record_and_transcribe`: Record audio for a specified duration and transcribe it

## Whisper Models

This extension supports various Whisper model sizes:

| Model | Speed | Accuracy | Memory Usage | Use Case |
|-------|-------|----------|--------------|----------|
| `tiny.en` | Fastest | Lowest | Minimal | Testing, quick transcriptions |
| `base.en` | Fast | Good | Low | Everyday use (default) |
| `small.en` | Medium | Better | Moderate | Good balance |
| `medium.en` | Slow | High | High | Important recordings |
| `large` | Slowest | Highest | Very High | Critical transcriptions |

The `.en` suffix indicates models specialized for English, which are faster and more accurate for English content.

## Requirements

- Python 3.12+
- An audio input device (microphone)

## Configuration

You can configure the server using environment variables:

```bash
# Set Whisper model
export WHISPER_MODEL=small.en

# Set audio sample rate
export SAMPLE_RATE=44100

# Set maximum recording duration (seconds)
export MAX_DURATION=120

# Then run the server
voice-recorder-mcp
```

## Troubleshooting

### Common Issues

- **No audio being recorded**: Check your microphone permissions and settings
- **Model download errors**: Ensure you have a stable internet connection for the initial model download
- **Integration with Goose**: Make sure the command path is correct
- **Audio quality issues**: Try adjusting the sample rate (default: 16000)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
