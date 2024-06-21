import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit, QDockWidget
from PyQt5.QtCore import Qt

from ui.model import Model
import handlers.ai_handler as ai_handler

class ConfigDock(QDockWidget):
    def __init__(self, model: Model, config_class: type) -> None:
        """
        Initialize the ConfigDock.

        Args:
            model (Model): The model instance.
            config_class (type): The configuration class.
        """
        super().__init__()
        self.setWindowTitle(config_class.NAME)
        self.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        self.model = model
        self.config_class = config_class
        
        default_path = os.path.join(ai_handler.__file__, self.config_class.DEFAULT_PATH)
        self.config_path = default_path if os.path.exists(default_path) else None
        self.main_widget = QWidget()
        self.main_widget.setMinimumWidth(200)  # Set the minimum width
        self.layout = QVBoxLayout(self.main_widget)

        self.create_view()
        self.setWidget(self.main_widget)

        if self.config_path:
            self.load_config()

    def create_view(self) -> None:
        """
        Create the view for the configuration dock.
        """
        self.settings_layout = QVBoxLayout()
        self.settings_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        ## Horizontal layout for the config load button
        self.config_layout = QHBoxLayout()
        self.parameters_layout = QVBoxLayout()
        self.load_config_button = QPushButton("Load Config")
        self.save_config_button = QPushButton("Save Config")
        self.load_config_button.clicked.connect(self.set_config_path)
        self.save_config_button.clicked.connect(self.save_config)

        self.config_label = QLabel("No config loaded")

        self.config_layout.addWidget(self.save_config_button)
        self.config_layout.addWidget(self.load_config_button)
        self.config_layout.addWidget(self.config_label)
        
        self.settings_layout.addLayout(self.config_layout)
        self.settings_layout.addLayout(self.parameters_layout)

        self.layout.addLayout(self.settings_layout)

    def set_config_path(self) -> None:
        """
        Set the configuration file path.
        """
        options = QFileDialog.Options()
        self.config_path, _ = QFileDialog.getOpenFileName(
            self, "Load Config File", "", "YAML Files (*.yml);;All Files (*)", options=options
        )
        self.load_config()

    def load_config(self) -> None:
        """
        Load the configuration from the file.
        """
        if self.config_path:
            self.model.set_config(self, self.config_path)
            self.config_label.setText(f"Config loaded: {self.config_path}")
            self.populate_config_form(self.model.configs[self.config_class.NAME])

    def save_config(self) -> None:
        """
        Save the current configuration to the file.
        """
        self.model.save_config(self)

    def set_config_parameters(self, label: str, value: str) -> None:
        """
        Set the configuration parameters.

        Args:
            label (str): The configuration parameter label.
            value (str): The configuration parameter value.
        """
        self.model.change_config_value(self, label, value)
    
    def populate_config_form(self, config) -> None:
        """
        Populate the configuration form with current settings.

        Args:
            config: The configuration instance.
        """

        #Clear layout if it has widgets
        layout = self.parameters_layout

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None and widget is not QPushButton:
                widget.deleteLater()
            

        parameters = QVBoxLayout()
        for var_name, var_value in config.config.items():
            widget = QWidget()
            layout = QHBoxLayout(widget)
            label_text = QLabel(str(var_name).replace('_', ' ').title())
            input_field = QLineEdit(self)
            input_field.setText(str(var_value))
            input_field.textChanged.connect(lambda text, vn=var_name: self.set_config_parameters(vn, text))

            layout.addWidget(label_text)
            layout.addWidget(input_field)
            
            parameters.addWidget(widget)
        
        self.parameters_layout.addLayout(parameters)
        self.reload_view()

    def reload_view(self) -> None:
        """
        Reload the view to reflect changes.
        """
        self.update()
        self.repaint()