import yaml
from typing import Any, Dict


class Config:
    def __init__(self, config_path: str):
        """
        Initialize the Config class.

        Args:
            config_path (str): The path to the configuration file.
        """
        self.config_path = config_path
        loaded_config = self.load()
        self.verify_config(loaded_config)
        self.config = {key: value for key, value in loaded_config.items()}

    def load(self) -> Dict[str, Any]:
        """
        Load the configuration from a YAML file.

        Returns:
            Dict[str, Any]: The loaded configuration.
        """
        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def save(self) -> None:
        """
        Save the current configuration to a YAML file.
        """
        print(self.config)
        with open(self.config_path, 'w') as file:
            yaml.dump(self.config, file, default_flow_style=False)
        print("Saved Config")

    def verify_config(self, config: Dict[str, Any]) -> None:
        """
        Verify the configuration.

        Args:
            config (Dict[str, Any]): The configuration dictionary.
        
        This method should be overridden by subclasses to provide specific
        verification logic for their configurations.
        """
        pass
        # Implement verification logic here