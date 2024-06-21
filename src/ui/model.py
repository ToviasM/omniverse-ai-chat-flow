import importlib
from threading import Thread

from ui.signal import application_signal
from loop import RecordingLoop
from handlers.ai_handler import AIConfig
from handlers.audio_handler import AudioConfig
from handlers.network.client import NetworkConfig, RestClient

class Model:
    def __init__(self):
        """
        Initialize the Model class.
        """
        self.configs = {}
        self.recording_loop = None
        self.recording_thread = None
        self.stop_recording = False
        
        self.network = None

        # Connect the shutdown signal to stop_audio method
        application_signal.shutdownSignal.connect(self.stop_audio)

    def set_config(self, config, config_path: str) -> None:
        """
        Set configuration for a given config class and path.

        Args:
            config: The configuration class instance.
            config_path (str): The path to the configuration file.
        """
        config_handler = config.config_class(config_path)
        self.configs[config.config_class.NAME] = config_handler

    def save_config(self, config) -> None:
        """
        Save the current configuration.

        Args:
            config: The configuration class instance.
        """
        if config.config_class.NAME in self.configs:
            self.configs[config.config_class.NAME].save()
        else:
            print("No Config has been selected to save!")

    def change_config_value(self, config, label: str, value: str) -> None:
        """
        Change a configuration value.

        Args:
            config: The configuration class instance.
            label (str): The configuration parameter label.
            value (str): The configuration parameter value.
        """
        if config.config_class.NAME in self.configs:
            self.configs[config.config_class.NAME].config[label] = value
        else:
            print("Config was not added to core Model List. This is an error")

    def get_ai_class(self, module_string: str):
        """
        Dynamically import and return a class from a module string.

        Args:
            module_string (str): The module path string.

        Returns:
            class: The dynamically imported class.
        """
        *module_path_parts, class_name = module_string.split('.')
        module_path = '.'.join(module_path_parts)
        module = importlib.import_module(module_path)
        handler_class = getattr(module, class_name)
        return handler_class

    def test_ai_response(self) -> str:
        """
        Test the AI response.

        Returns:
            str: The AI response message.
        """
        config = self.configs[AIConfig.NAME]

        if config:
            if application_signal:
                ai_class = self.get_ai_class(config.config.get("module"))
                service = ai_class(**config.config)
                response = service.get_response("What is the weather in Denmark?")
                message = f"{service.NAME} : {response.content}"
                application_signal.addResponseWidgetSignal.emit(message)
                application_signal.closeDialogSignal.emit()
                return message
        
        return "Config not loaded"

    def test_audio(self) -> None:
        """
        Test audio recording.
        """
        config = self.configs[AIConfig.NAME]
        if config:
            if application_signal:
                if not self.recording_loop:
                    ai_class = self.get_ai_class(config.config.get("module"))
                    service = ai_class(**config.config)
                    self.recording_loop = RecordingLoop(ai_service=service, **self.configs[AudioConfig.NAME].config)
                    
                    self.stop_recording = False
                    self.recording_thread = Thread(target=self.recording_loop.test_record, args=(id, lambda: self.stop_recording))
                    self.recording_thread.start()

    def live_audio(self) -> None:
        """
        Start live audio recording and interaction.
        """
        config = self.configs[AIConfig.NAME]
        if config:
            if application_signal:
                if not self.recording_loop:
                    ai_class = self.get_ai_class(config.config.get("module"))
                    service = ai_class(**config.config)
                    self.recording_loop = RecordingLoop(ai_service=service, **self.configs[AudioConfig.NAME].config)
                    
                    self.stop_recording = False
                    self.recording_thread = Thread(target=self.recording_loop.start_live, args=(id, lambda: self.stop_recording, self.send_network_message))
                    self.recording_thread.start()

    def stop_audio(self) -> None:
        """
        Stop the audio recording.
        """
        if self.configs[AIConfig.NAME]:
            if application_signal:
                if self.recording_loop:
                    application_signal.closeDialogSignal.emit()
                    self.stop_recording = True
                    self.recording_thread.join()

                self.recording_loop = None
                self.recording_thread = None

    def send_network_message(self, path) -> None:
        config = self.configs[NetworkConfig.NAME]
        if config:
            if application_signal:
                if self.recording_loop:
                    if self.network == None:
                        self.network = RestClient(**config.config)
                    self.network.send_text(text=path)