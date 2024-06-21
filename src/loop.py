import os
import keyboard
import sounddevice as sd
import soundfile as sf
from enum import Enum

from handlers.audio_handler import VoiceRecorder
from ui.signal import application_signal


class RecordingLoop:
    def __init__(self, path: str, filename: str, ai_service, sample_rate: int, recording_key: str, **kwargs):
        """
        Initialize the RecordingLoop instance.

        Args:
            path (str): The directory path to save recordings.
            filename (str): The base filename for recordings.
            ai_service: The AI service for transcribing and responding.
            sample_rate (int): The sample rate for recording.
            recording_key (str): The key to start recording.
            **kwargs: Additional arguments.
        """
        self.recorder = VoiceRecorder(sample_rate=int(sample_rate))
        self.ai_service = ai_service
        self.recording_key = recording_key
        self.path = path
        self.file_index = 0
        self.filename = filename

        self.is_recording = False

        ## Connect the signal to stop playing audio
        application_signal.closeDialogSignal.connect(self.stop_playing)

    def stop_playing(self) -> None:
        """
        Stop any currently playing audio.
        """
        sd.stop()

    def test_record(self, id: int, stop: callable) -> None:
        """
        Test recording loop.

        Args:
            id (int): An identifier for the recording session.
            stop (callable): A callable to determine if the loop should stop.
        """
        while True:
            if stop():
                ## Exit the loop if the stop condition is met
                print("Exiting loop.")
                self.is_recording = False
                break

            if keyboard.is_pressed(self.recording_key):
                if self.is_recording == False:
                    application_signal.isRecording.emit("RECORDING")
                    self.is_recording = True
                ## Generate the file path for the new recording
                file_path = os.path.join(self.path, f"{self.filename}_{self.file_index}.wav")
                self.file_index += 1
                ## Record and play the audio
                self.recorder.record(file_path, self.recording_key)
                application_signal.isRecording.emit("PLAYING")
                self.recorder.play(file_path)
            elif self.is_recording == True:
                application_signal.isRecording.emit("USER")
                self.is_recording = False
                

    def start_live(self, id: int, stop: callable, callback: callable) -> None:
        """
        Live recording and interaction loop.

        Args:
            id (int): An identifier for the recording session.
            stop (callable): A callable to determine if the loop should stop.
        """
        while True:
            if stop():
                ## Exit the loop if the stop condition is met
                print("Exiting loop.")
                break

            if keyboard.is_pressed(self.recording_key):
                if self.is_recording == False:
                    application_signal.isRecording.emit("RECORDING")
                    self.is_recording = True
                ## Generate the file path for the new recording
                file_path = self.path + "/" + f"{self.filename}_{self.file_index}.wav"
                self.file_index += 1
                ## Record the audio
                self.recorder.record(file_path, self.recording_key)
                application_signal.isRecording.emit("WAITING")
                ## Transcribe the audio file
                question = self.ai_service.transcribe_audio_file(file_path)
                question_message = f"USER : {question}"
                ## Emit the transcribed question signal
                application_signal.addResponseWidgetSignal.emit(question_message)

                ## Get the AI response
                text_response = self.ai_service.get_response(question)
                response_message = f"{self.ai_service.NAME} : {text_response.content}"
                ## Emit the AI response signal
                application_signal.addResponseWidgetSignal.emit(response_message)

                ## Convert the AI response to speech and play it
                voice_response_file = file_path.replace(".wav", "_bot.wav")
                self.ai_service.text_to_speech(text_response.content, voice_response_file)
                application_signal.isRecording.emit("PLAYING")
                
                #Send path to callback, then play. In most cases it sends it to the network
                with sf.SoundFile(voice_response_file, mode='r') as sound_file:
                    callback(voice_response_file)
                #self.recorder.play(voice_response_file)
            elif self.is_recording == True:
                application_signal.isRecording.emit("USER")
                self.is_recording = False