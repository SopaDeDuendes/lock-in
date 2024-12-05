from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea
)
from PyQt6.QtCore import Qt

class ActivityCard(QWidget):
    def __init__(self, activity_name, total_time, details):
        super().__init__()
        
        self.setStyleSheet("""
            QWidget {
                background-color: #FFFFFF;
                border-radius: 8px;
                border: 1px solid #DDDDDD;
                padding: 10px;
                margin-bottom: 10px;
            }
            QLabel {
                font-size: 12px;
                color: #333333;
            }
            QPushButton {
                font-size: 10px;
                background-color: #4CAF50;  /* Fondo verde */
                color: #FFFFFF;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Layout principal
        layout = QVBoxLayout(self)

        # Widget de nombre de actividad y tiempo total
        activity_layout = QHBoxLayout()
        self.activity_label = QLabel(f"Actividad: {activity_name}", self)
        self.time_label = QLabel(f"Tiempo Total: {total_time} min", self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        activity_layout.addWidget(self.activity_label)
        activity_layout.addWidget(self.time_label)

        # Botón de detalles
        self.details_button = QPushButton("Detalles", self)
        self.details_button.clicked.connect(self.show_details)
        
        # Etiqueta de detalles
        self.details_label = QLabel("Detalles:", self)
        self.details_label.setStyleSheet("font-weight: bold;")

        # Área de detalles (oculta inicialmente)
        self.details_area = QScrollArea(self)
        self.details_area.setWidgetResizable(True)
        self.details_area.setWidget(QLabel(details, self))
        self.details_area.setVisible(False)  # Inicialmente oculto

        layout.addLayout(activity_layout)
        layout.addWidget(self.details_button)
        layout.addWidget(self.details_label)
        layout.addWidget(self.details_area)

    def show_details(self):
        # Mostrar u ocultar los detalles
        current_visibility = self.details_area.isVisible()
        self.details_area.setVisible(not current_visibility)
        text = "Ocultar Detalles" if not current_visibility else "Detalles"
        self.details_button.setText(text)
