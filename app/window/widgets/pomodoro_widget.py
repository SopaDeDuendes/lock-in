import time
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QHBoxLayout, QSpacerItem, QSizePolicy

class TimerPopup(QDialog):
    def __init__(self, topic_name, time_minutes, parent=None):
        super().__init__(parent)

        # Configurar la ventana sin bordes y con fondo translúcido
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Fondo translúcido
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.5); border-radius: 10px;")
        
        # Ajustar el tamaño de la ventana según sea necesario
        self.setFixedSize(350, 50)

        # Variables de tiempo
        self.time_minutes = time_minutes
        self.time_left = self.time_minutes * 60  # Convertir los minutos a segundos

        # Layout principal en fila (Horizontal)
        layout = QHBoxLayout()

        # Etiqueta para mostrar el nombre del tema
        self.topic_label = QLabel(topic_name, self)
        self.topic_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold;")
        self.topic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.topic_label.setWordWrap(True)  # Permitir que el texto se divida en varias líneas
        layout.addWidget(self.topic_label)

      

        # Mostrar tiempo restante en formato MM:SS
        self.time_label = QLabel(f"{self.time_minutes:02}:00", self)
        self.time_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.time_label)

        # Configurar temporizador
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(1000)  # Actualiza cada segundo

        # Iniciar la ventana con el layout
        self.setLayout(layout)

        # Posicionar la ventana en la parte superior, centrada
        self.center_top()

    def center_top(self):
        # Obtener la geometría de la pantalla
        screen_geometry = self.screen().geometry()

        # Calcular la posición central en la parte superior
        x_pos = (screen_geometry.width() - self.width()) // 2
        y_pos = 0  # Parte superior de la pantalla

        # Mover el widget a la posición deseada
        self.move(x_pos, y_pos)

    def update_progress(self):
        # Actualizar el tiempo restante
        if self.time_left > 0:
            self.time_left -= 1  # Decrementar el tiempo restante en segundos
            minutes, seconds = divmod(self.time_left, 60)
            self.time_label.setText(f"{minutes:02}:{seconds:02}")
        else:
            self.timer.stop()  # Detener el temporizador cuando el tiempo se agote
            self.close()  # Cerrar el popup cuando se termine el temporizador


if __name__ == "__main__":
    app = QApplication([])

    # Crear una instancia de la ventana con el tema y tiempo (en minutos)
    popup = TimerPopup("Cálculo Diferencial", 5)

    popup.exec()

    app.exec()
