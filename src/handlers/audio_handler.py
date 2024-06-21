import sounddevice as sd
import soundfile as sf
import numpy as np
import webrtcvad
import keyboard
import sys
import queue

from config import Config


class AudioConfig(Config):
    NAME = "AUDIO_CONFIG"
    DEFAULT_PATH = "../../../configs/audio_config.yml"

    def __init__(self, config_path: str):
        """
        Initialize the AudioConfig class.

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


class VoiceRecorder:
    def __init__(self, device: dict = None, sample_rate: int = 44100, channel_count: int = 2, chunk_duration_ms: int = 30):
        """
        Initialize the VoiceRecorder class.

        Args:
            device (dict): The audio device configuration.
            sample_rate (int): The sample rate for recording.
            channel_count (int): The number of audio channels.
            chunk_duration_ms (int): The duration of each audio chunk in milliseconds.
        """
        if device:
            self.device = device.get("name")
        else:
            devices = sd.query_devices()
            self.device = devices[int(1)].get("name")

        self.sample_rate = sample_rate
        self.channel_count = channel_count
        self.chunk_size = int(sample_rate * chunk_duration_ms / 1000)  # Convert from ms to samples
        self.vad = webrtcvad.Vad(1)  # 0 to 3, where 3 is the most aggressive
        self.recording = np.array([])
        self.q = queue.Queue()

    def record(self, file: str, key: str) -> None:
        """
        Record audio while the specified key is held down.

        Args:
            file (str): The file path to save the recording.
            key (str): The key to hold down for recording.
        """
        with sf.SoundFile(file, mode='w', samplerate=self.sample_rate, channels=self.channel_count) as sound_file:
            with sd.InputStream(samplerate=self.sample_rate, device=self.device, channels=self.channel_count, callback=self.callback):
                print('#' * 80)
                print('Press the specified key to stop the recording')
                print('#' * 80)
                while keyboard.is_pressed(key):
                    sound_file.write(self.q.get())
                print("Recording stopped")

    def callback(self, indata: np.ndarray, frames: int, time, status) -> None:
        """
        This is called (from a separate thread) for each audio block.

        Args:
            indata (np.ndarray): The recorded audio data.
            frames (int): The number of frames.
            time: The time information.
            status: The status of the recording.
        """
        if status:
            print(status, file=sys.stderr)
        self.q.put(indata.copy())

    def play(self, file: str) -> None:
        """
        Play the recorded file.

        Args:
            file (str): The file path of the recording to play.
        """
        with sf.SoundFile(file, mode='r') as sound_file:
            data = sound_file.read(dtype='float32')
            sd.play(data, samplerate=26000)
            sd.wait()