from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget, QAction, QToolBar
from PyQt5.QtCore import Qt, QTimer

from ui.model import Model
from ui.signal import application_signal
import handlers.ai_handler as ai_handler
from handlers.ai_handler import AIConfig
from handlers.audio_handler import AudioConfig
from handlers.network.client import NetworkConfig
from ui.widgets.dialog import SignalDialog
from ui.widgets.docks import ConfigDock
from ui.widgets.widgets import CenterResponseWidget

class MainView(QMainWindow):
    def __init__(self):
        """
        Initialize the MainView.
        """
        super().__init__()

        model = Model()

        config_dock = ConfigDock(model, AIConfig)
        audio_config_dock = ConfigDock(model, AudioConfig)
        network_dock = ConfigDock(model, NetworkConfig)

        response_widget = CenterResponseWidget(model)

        self.setWindowTitle("Omniverse AI Service")
        self.setGeometry(100, 100, 1500, 700)
        self.setCentralWidget(response_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, config_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, audio_config_dock)
        self.addDockWidget(Qt.RightDockWidgetArea, network_dock)

        ## Create toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        ## Add actions to toolbar for showing/hiding docks
        config_dock_action = QAction("Config Dock", self)
        config_dock_action.setCheckable(True)
        config_dock_action.setChecked(True)
        config_dock_action.triggered.connect(lambda: self.toggle_dock(config_dock))

        audio_config_dock_action = QAction("Audio Config Dock", self)
        audio_config_dock_action.setCheckable(True)
        audio_config_dock_action.setChecked(True)
        audio_config_dock_action.triggered.connect(lambda: self.toggle_dock(audio_config_dock))

        network_dock_action = QAction("Network Config Dock", self)
        network_dock_action.setCheckable(True)
        network_dock_action.setChecked(True)
        network_dock_action.triggered.connect(lambda: self.toggle_dock(network_dock))

        toolbar.addAction(config_dock_action)
        toolbar.addAction(audio_config_dock_action)
        toolbar.addAction(network_dock_action)
        
        self.resize_docks([config_dock, audio_config_dock], [300, 300])

    def resize_docks(self, docks: list, sizes: list) -> None:
        """
        Resize the docks.

        Args:
            docks (list): List of docks to resize.
            sizes (list): List of sizes for the docks.
        """
        self.resizeDocks(docks, sizes, Qt.Horizontal)

    def toggle_dock(self, dock_widget: QDockWidget) -> None:
        """
        Toggle the visibility of a dock widget.

        Args:
            dock_widget (QDockWidget): The dock widget to toggle.
        """
        if dock_widget.isVisible():
            dock_widget.hide()
        else:
            dock_widget.show()

    def closeEvent(self, event) -> None:
        """
        Handle the close event.

        Args:
            event: The close event.
        """
        application_signal.shutdownSignal.emit()
        QTimer.singleShot(1000, self.close_application)
        event.ignore()

    def close_application(self) -> None:
        """
        Force close the application.
        """
        QApplication.instance().quit()