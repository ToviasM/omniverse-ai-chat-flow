# Python AI Chat Flow For Omniverse & Unreal

This repository contains an AI-powered REST client implemented in Python using PyQt for the graphical user interface. The client can automatically record audio, transcribe it to text using an AI model, send the transcribed text to an AI model to get a response, convert the response back to speech, and send the resulting audio file to a REST API endpoint.

## Features

- **Automatic Workflow**: Record audio, transcribe it, get an AI response, convert the response to speech, and send the resulting audio file to a server.
- **GUI Configuration**: Configure AI, audio, and network settings through an intuitive GUI.
- **Audio Recording**: Record audio using your microphone.
- **AI Transcription**: Transcribe recorded audio to text using an AI model.
- **AI Response**: Send transcribed text to an AI model to get a response.
- **Text-to-Speech**: Convert the AI's text response to speech.
- **REST Client**: Send audio files and text strings to a specified REST API endpoint.
- **Error Handling**: Comprehensive error handling for HTTP requests and file operations.

## Requirements

- Python 3.6 or later
- `requests` library
- `sounddevice` library
- `soundfile` library
- `PyYAML` library
- `webrtcvad` library
- `keyboard` library
- `PyQt5` library

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ToviasM/python-ai-chat-flow/edit/
    cd omniverse-ai-service
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Setup your .env file to incorporate your API keys.
   
3. Update the configuration files located in the `configs` directory to match your setup.

4. Run the application:
    ```sh
    python main.py
    ```

5. Use the GUI to configure AI, audio, and network settings.

    - **AI Config**: Set the chat model, module, speech model, system message, transcribe model, and voice.
    - **Audio Config**: Set the audio device, filename, path, recording key, and sample rate.
    - **Network Config**: Set the base URL, endpoint, folder path, and instance name.

6. Use the buttons at the bottom of the GUI to:
    - **Test AI Response**: Test the AI's response.
    - **Audio Playback**: Test audio playback.
    - **Go Live**: Start live audio recording and interaction.

## Example

Here is an example of how the application workflow operates:

1. **Recording**: Press and hold the configured recording key to start recording audio.
2. **Transcription**: The recorded audio is automatically transcribed to text using the configured AI transcription model.
3. **AI Response**: The transcribed text is sent to the configured AI model, and a response is generated.
4. **Text-to-Speech**: The AI's text response is converted to speech.
5. **REST Call**: The resulting audio file is sent to the specified REST API endpoint.
