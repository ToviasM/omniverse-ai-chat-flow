from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QPainter, QColor

from ui.signal import application_signal

STATUS = {
    "USER" : "red",
    "RECORDING" : "green",
    "WAITING" : "yellow",
    "PLAYING" : "blue",
}
class CircleWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color = QColor('red')
        application_signal.isRecording.connect(self.set_color)

    @pyqtSlot(str)
    def set_color(self, status):
        self.color = QColor(STATUS[status])
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        painter.setPen(Qt.NoPen)
        size = min(self.width(), self.height())
        painter.drawEllipse(int((self.width() - size) / 2), int((self.height() - size) / 2), int(size), int(size))


class SignalDialog(QDialog):
    def __init__(self, parent: QWidget, title: str, message: str, button_text: str = "", callback: callable = None):
        """
        Initialize the SignalDialog.

        Args:
            parent (QWidget): The parent widget.
            title (str): The title of the dialog.
            message (str): The message to display in the dialog.
            button_text (str): The text for the button (optional).
            callback (callable): The function to call when the button is clicked (optional).
        """
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 400, 200)

        # Set up the layout and label
        layout = QVBoxLayout()
        label = QLabel(message)
        layout.addWidget(label)

        live_widget = CircleWidget(self)
        layout.addWidget(live_widget)
        
        if callback:
            button = QPushButton(button_text)
            button.clicked.connect(callback)
            layout.addWidget(button)
        
        self.setLayout(layout)

        ## Connect the signal to close the dialog
        application_signal.closeDialogSignal.connect(self.accept)