from PyQt6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QDialog, QPushButton
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator


class TimerDialog(QDialog):
    def __init__(self, parent=None, current_time=0):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)  # Sin barra de título
        self.setModal(True)  # Modales para bloquear interacción con la ventana principal
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)  # Habilitar estilos personalizados

        # Cambiar fondo del diálogo completo a gris claro con bordes redondeados
        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E1E;  /* Fondo gris oscuro */
                border-radius: 15px;         /* Bordes redondeados */
                border: 2px solid #BBBBBB;   /* Borde claro */
                padding: 12px;
            }
            QLabel {
                font-size: 10px;  /* Fuente más pequeña */
                color: #FFFFFF;   /* Color blanco para las etiquetas */
            }
            QLineEdit {
                font-size: 12px;  /* Fuente más pequeña */
                color: #FFFFFF;   /* Color blanco para el texto */
                background-color: #444444;  /* Fondo de entrada oscuro */
                border: 1px solid #888888;  /* Borde gris */
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton {
                font-size: 10px;  /* Fuente más pequeña */
                padding: 5px 10px;
                background-color: #5C5C5C;  /* Fondo de los botones */
                color: #FFFFFF;
                border-radius: 8px;  /* Bordes redondeados para los botones */
            }
            QPushButton:hover {
                background-color: #444444;  /* Color de fondo al pasar el cursor */
            }
        """)

        self.setFixedSize(200, 120)  # Tamaño del diálogo ajustado
        # Layout principal
        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(4)  # Espaciado entre elementos

        # Etiqueta informativa sobre el rango (antes era un placeholder en QLineEdit)
        self.info_label = QLabel("Pomodoro: 5 ~ 180 minutos.", self)
        self.layout.addWidget(self.info_label)

        # Layout horizontal para el input de tiempo
        time_layout = QHBoxLayout()
        self.time_input = QLineEdit(self)
        self.time_input.setValidator(QIntValidator(5, 180, self))  # Solo números entre 5 y 180
        
        # Si el valor actual es pasado, asignarlo solo si el campo está vacío
        if current_time > 0 and not self.time_input.text():
            self.time_input.setText(str(current_time))  # Valor inicial
        self.time_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.min_label = QLabel("min", self)
        time_layout.addWidget(self.time_input)
        time_layout.addWidget(self.min_label)
        self.layout.addLayout(time_layout)

        # Botones "Aceptar" y "Cancelar"
        button_layout = QHBoxLayout()
        self.accept_button = QPushButton("Aceptar", self)
        self.accept_button.clicked.connect(self.accept)  # Guardar cambios y cerrar
        self.cancel_button = QPushButton("Cancelar", self)
        self.cancel_button.clicked.connect(self.reject)  # Descartar cambios y cerrar
        button_layout.addWidget(self.accept_button)
        button_layout.addWidget(self.cancel_button)
        self.layout.addLayout(button_layout)

    def get_time(self):
        """Devuelve el tiempo configurado como un entero."""
        try:
            return int(self.time_input.text())
        except ValueError:
            return 0
