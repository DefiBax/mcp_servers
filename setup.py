from setuptools import setup, find_packages

setup(
    name="voice-recorder-mcp",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "voice-recorder-mcp=voice_recorder:main",
        ],
    },
)
