from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget, QApplication
from PyQt6.QtGui import QFont
import sys

class SplashScreen(QMainWindow):
    finished = pyqtSignal()  # Señal para indicar que el splash ha terminado

    def __init__(self):
        super().__init__()

        # Configuración de la ventana (sin bordes y con fondo transparente)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(600, 400)  # Tamaño de la ventana 600x400

        # Fondo oscuro de terminal
        self.centralwidget = QWidget(self)
        self.centralwidget.setStyleSheet("background-color: #1E1E1E; border-radius: 20px;")
        self.setCentralWidget(self.centralwidget)

        # Layout principal (vertical para apilar los elementos)
        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Gato ASCII con texto "LOCK - IN"
        self.cat_ascii = """
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⣼⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣠⣤⣤⣼⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀
⠀⠀⠀⢀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀
⠀⠀⠀⠘⣿⣿⣿⣿⠟⠁⠀⠀⠀⠹⣿⣿⣿⣿⣿⠟⠁⠀⠀⠹⣿⣿⡿⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀⠀⢼⣿⠀⢿⣿⣿⣿⣿⠀⣾⣷⠀⠀⢿⣿⣷⠀⠀⠀⠀⠀
⠀⠀⠀⢠⣿⣿⣿⣷⡀⠀⠀⠈⠋⢀⣿⣿⣿⣿⣿⡀⠙⠋⠀⢀⣾⣿⣿⠀⠀⠀⠀⠀
⢀⣀⣀⣀⣿⣿⣿⣿⣿⣶⣶⣶⣶⣿⣿⣿⣿⣾⣿⣷⣦⣤⣴⣿⣿⣿⣿⣤⠤⢤⣤⡄
⠈⠉⠉⢉⣙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⣀⣀⣀⡀⠀
⠐⠚⠋⠉⢀⣬⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣥⣀⡀⠈⠀⠈⠛
⠀⠀⠴⠚⠉⠀⠀⠀⠉⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠋⠁⠀⠀⠀⠉⠛⠢⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀
        """

        # Etiqueta para mostrar el gato y "LOCK - IN"
        self.cat_label = QLabel(self.cat_ascii, self)

        self.cat_label.setStyleSheet("color: #ae76ff; font-size: 10px;")
        self.cat_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.lockin_label = QLabel("LOCK - IN", self)
        self.lockin_label.setStyleSheet("color: #ae76ff; font-size: 32px;")
        self.lockin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Widget de barra de carga con ASCII
        self.progress_label = QLabel(self)
        self.progress_label.setStyleSheet("color: #ae76ff;font-size: 14px;")
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Añadimos los elementos al layout
        self.layout.addWidget(self.cat_label)
        self.layout.addWidget(self.lockin_label)
        self.layout.addWidget(self.progress_label)

        # Inicializar los valores de la barra de progreso
        self.progress = 0
        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress)
        self.progress_timer.start(500)  # Actualiza cada 500ms

        # Temporizador para finalizar la animación en 5 segundos
        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.finish_loading)
        self.animation_timer.start(3000)  # 5 segundos

    def update_progress(self):
        """Actualiza la barra de carga ASCII."""
        self.progress += 20  # Aumenta el progreso de forma más rápida para completar en 5 segundos
        if self.progress > 100:
            self.progress = 100
        
        # Crear la barra de progreso con ASCII
        progress_bar = "[" + "=" * (self.progress // 10) + "-" * (10 - self.progress // 10) + "]"
        self.progress_label.setText(f"{progress_bar} {self.progress}%")
        
        if self.progress == 100:
            self.progress_timer.stop()

    def finish_loading(self):
        """Finaliza la pantalla de carga y cierra el splash."""
        self.animation_timer.stop()
        self.finished.emit()  # Emitir señal cuando la pantalla de carga termine
        self.close()  # Cerrar la pantalla de splash

