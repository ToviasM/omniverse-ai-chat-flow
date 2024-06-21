import requests
import os

from config import Config

class NetworkConfig(Config):
    NAME = "NETWORK_CONFIG"
    DEFAULT_PATH = "../../../configs/network.yml"

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


##This class can be further implemented to send audio files over to another computer doing the audio calculations. For now, we will be sending file location locally
class RestClient:
    def __init__(self, endpoint:str, base_url: str, instance_name: str, **kwargs):
        """
        Initialize the RestClient with the base URL of the REST API.

        Args:
            base_url (str): The base URL of the REST API.
        """
        self.endpoint = endpoint
        self.base_url = base_url
        self.instance_name = instance_name

    def send_audio_file(self, file_path: str):
        """
        Send an audio file to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the audio file to.
            file_path (str): The path to the audio file.
        
        Returns:
            Response: The HTTP response from the server.
        """
        url = str(os.path.join(self.base_url, self.endpoint))
        print(url)
        files = {'file': open(file_path, 'rb')}
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()  # Raise an error for bad status codes
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None
        
    def send_text(self, text: str):
        """
        Send a string to the specified endpoint.

        Args:
            endpoint (str): The endpoint to send the string to.
            text (str): The string to send.
        
        Returns:
            Response: The HTTP response from the server.
        """
        url = self.base_url + "/" + self.endpoint
        
        data = {'path': text, 'instance_name': self.instance_name}
        print(url)
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()  # Raise an error for bad status codes
            return response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None


# if __name__ == "__main__":
#     # Example usage
#     base_url = "http://localhost:5000"
#     endpoint = "upload_audio"
#     file_path = "path/to/your/audio/file.wav"

#     client = RestClient(base_url)
#     response = client.send_audio_file(endpoint, file_path)

#     if response:
#         print("File uploaded successfully!")
#         print("Server response:", response.json())
#     else:
#         print("Failed to upload the file.")