from PyQt5.QtCore import pyqtSignal, QObject

class Communicate(QObject):
    addResponseWidgetSignal = pyqtSignal(str)
    closeDialogSignal = pyqtSignal()
    shutdownSignal = pyqtSignal()
    isRecording = pyqtSignal(str)

# A global instance of Communicate
application_signal = Communicate()