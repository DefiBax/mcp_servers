import os
import argparse
from dataclasses import dataclass


@dataclass
class Config:
    whisper_model: str = "base.en"
    sample_rate: int = 16000
    max_duration: int = 60


def parse_args():
    parser = argparse.ArgumentParser(
        description="MCP server for voice recording and transcription using Whisper."
    )
    parser.add_argument('--model', default='base.en', help='Whisper model to use')
    parser.add_argument('--sample-rate', type=int, default=16000, help='Audio sample rate')
    return parser.parse_args()


def get_config():
    """Load configuration from environment variables or command line arguments"""
    args = parse_args()

    # Environment variables take precedence over command line arguments
    config = Config(
        whisper_model=os.environ.get("WHISPER_MODEL", args.model),
        sample_rate=int(os.environ.get("SAMPLE_RATE", args.sample_rate)),
        max_duration=int(os.environ.get("MAX_DURATION", 60))
    )

    return config