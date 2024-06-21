from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QScrollArea, QSizePolicy
from PyQt5.QtCore import Qt

from ui.model import Model
from ui.signal import application_signal
from handlers.audio_handler import AudioConfig
from ui.widgets.dialog import SignalDialog


class CenterResponseWidget(QWidget):
    def __init__(self, model: Model) -> None:
        """
        Initialize the AIResponseWidget.

        Args:
            model (Model): The model instance.
        """
        super().__init__()
        self.model = model

        self.layout = QVBoxLayout()
        self.create_view()
        self.setLayout(self.layout)
    
    def create_view(self) -> None:
        """
        Create the view for the AI response widget.
        """
        ## Main layout for the response widget
        main_layout = QVBoxLayout()
        
        self.scroll = QScrollArea()
        widget = QWidget()          
        self.log_layout = QVBoxLayout(widget)
        self.log_layout.setAlignment(Qt.AlignTop)

        application_signal.addResponseWidgetSignal.connect(self.add_response)

        ## Scroll area configuration
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Set expanding policy
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(widget)

        ## Buttons layout
        buttons_layout = QHBoxLayout()
        
        test_button = QPushButton("Test AI Response")
        test_button.clicked.connect(self.test_ai_response)
        buttons_layout.addWidget(test_button)
        
        record_button = QPushButton("Audio Play Back")
        record_button.clicked.connect(self.test_audio_playback)
        buttons_layout.addWidget(record_button)
        
        live_button = QPushButton("Go Live")
        live_button.clicked.connect(self.live_recording)
        buttons_layout.addWidget(live_button)

        buttons_layout.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        main_layout.addWidget(self.scroll)
        main_layout.addLayout(buttons_layout)
        self.layout.addLayout(main_layout)

    def add_response(self, response: str) -> None:
        """
        Add a response to the log layout.

        Args:
            response (str): The response to add.
        """
        response_widget = QLabel(response)
        response_widget.setWordWrap(True)  # Enable word wrapping for the label
        response_widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        response_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)  # Set expanding policy

        self.log_layout.addWidget(response_widget)

    def test_ai_response(self) -> None:
        """
        Test AI response.
        """
        dialog = SignalDialog(self, title="Testing Audio Playback", message="Testing AI Response")
        dialog.show()
        self.model.test_ai_response()
    
    def test_audio_playback(self) -> None:
        """
        Test audio playback.
        """
        dialog = SignalDialog(
            self, title="Testing Audio Playback", 
            message=f"Hold {self.model.configs[AudioConfig.NAME].config.get('recording_key')} while speaking, let go when finished", 
            button_text="Stop Playback", callback=self.stop_recording
        )
        dialog.show()
        self.model.test_audio()

    def live_recording(self) -> None:
        """
        Start live recording and interaction.
        """
        dialog = SignalDialog(
            self, title="Testing Audio Playback", 
            message=f"Hold {self.model.configs[AudioConfig.NAME].config.get('recording_key')} while speaking, let go when finished. AI will respond back, wait for response before answering", 
            button_text="Stop Live", callback=self.stop_recording
        )
        dialog.show()
        self.model.live_audio()

    def stop_recording(self) -> None:
        """
        Stop the recording.
        """
        self.model.stop_audio()

