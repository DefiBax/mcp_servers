#!/bin/bash
# run.sh - Run the voice recorder MCP server with the MCP Inspector

# Change to the project root directory
cd "$(dirname "$0")"

# Set PYTHONPATH to include src directory
export PYTHONPATH="$PYTHONPATH:./src"

## Launch MCP inspector with the server directly
#npx @modelcontextprotocol/inspector python src/voice_recorder/server.py