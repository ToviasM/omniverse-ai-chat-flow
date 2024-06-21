from pathlib import Path

from config import Config


class AIConfig(Config):
    NAME = "AI_CONFIG"
    DEFAULT_PATH = "../../../configs/open_ai.yml"

    def __init__(self, config_path: str):
        """
        Initialize the AIConfig class.

        Args:
            config_path (str): The path to the configuration file.
        """
        super().__init__(config_path)
    
    def verify_config(self, config: dict) -> None:
        """
        Verify the configuration.

        Args:
            config (dict): The configuration dictionary.
        """
        pass


class AIHandler:
    def __init__(self, **kwargs):
        """
        Initialize the AIHandler class.
        
        Args:
            kwargs: Additional keyword arguments.
        """
        pass

    def get_response(self, question: str) -> str:
        """
        Get a response from the AI model.

        Args:
            question (str): The question to ask the AI.

        Returns:
            str: The AI's response.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def transcribe_audio_file(self, path: str) -> str:
        """
        Transcribe an audio file.

        Args:
            path (str): The path to the audio file.

        Returns:
            str: The transcription of the audio file.
        """
        raise NotImplementedError("Subclasses should implement this method")

    def text_to_speech(self, text: str, file_path: str) -> None:
        """
        Convert text to speech and save to a file.

        Args:
            text (str): The text to convert to speech.
            file_path (str): The path to save the speech file.
        """
        raise NotImplementedError("Subclasses should implement this method")


class OpenAIHandler(AIHandler):
    NAME = "OPEN_AI"

    def __init__(self, system_message: str, chat_model: str, transcribe_model: str, speech_model: str, voice: str, **kwargs):
        """
        Initialize the OpenAIHandler class.

        Args:
            system_message (str): The system message for the AI.
            chat_model (str): The chat model name.
            transcribe_model (str): The transcription model name.
            speech_model (str): The speech model name.
            voice (str): The voice to use for speech.
            kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

        from openai import OpenAI
        self.client = OpenAI()
        self.messages = [{"role": "system", "content": system_message}]

        self.system_message = system_message
        self.chat_model = chat_model
        self.transcribe_model = transcribe_model
        self.speech_model = speech_model
        self.voice = voice

    def transcribe_audio_file(self, path: str) -> str:
        """
        Transcribe an audio file using OpenAI.

        Args:
            path (str): The path to the audio file.

        Returns:
            str: The transcription of the audio file.
        """
        with open(path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model=self.transcribe_model,
                file=audio_file
            )
        return transcription.text

    def get_response(self, question: str) -> dict:
        """
        Get a response from the OpenAI model.

        Args:
            question (str): The question to ask the AI.

        Returns:
            dict: The AI's response.
        """
        self.messages.append({"role": "user", "content": question})

        response = self.client.chat.completions.create(
            model=self.chat_model,
            messages=self.messages
        )

        self.messages.append(response.choices[0].message)

        return response.choices[0].message

    def text_to_speech(self, text: str, file_path: str) -> None:
        """
        Convert text to speech using OpenAI and save to a file.

        Args:
            text (str): The text to convert to speech.
            file_path (str): The path to save the speech file.
        """
        speech_file_path = Path(file_path)
        response = self.client.audio.speech.create(
            model=self.speech_model,
            voice=self.voice,
            input=text
        )

        response.stream_to_file(speech_file_path)


class GeminiHandler(AIHandler):
    NAME = "GEMINI"

    def __init__(self, system_context: str, **kwargs):
        """
        Initialize the GeminiHandler class.

        Args:
            system_context (str): The system context for the AI.
            kwargs: Additional keyword arguments.
        """
        super().__init__(**kwargs)

    def transcribe_audio_file(self, path: str) -> str:
        """
        Transcribe an audio file using Gemini.

        Args:
            path (str): The path to the audio file.

        Returns:
            str: The transcription of the audio file.
        """
        pass

    def get_response(self, question: str) -> str:
        """
        Get a response from the Gemini model.

        Args:
            question (str): The question to ask the AI.

        Returns:
            str: The AI's response.
        """
        pass

    def text_to_speech(self, text: str, file_path: str) -> None:
        """
        Convert text to speech using Gemini and save to a file.

        Args:
            text (str): The text to convert to speech.
            file_path (str): The path to save the speech file.
        """
        pass