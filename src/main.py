import sys
from PyQt5.QtWidgets import QApplication

import qdarkstyle

from ui.view import MainView
from ui.signal import application_signal



def main() -> None:
    """
    The main function initializes the application, sets the stylesheet, shows the main view,
    and waits for the shutdown signal before closing.
    """
    app = QApplication(sys.argv)
    view = MainView()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    view.show()
    
    # Emit shutdown signal (comment suggests a 1-second wait, but not implemented here)
    application_signal.shutdownSignal.emit()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()