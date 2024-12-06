from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from splash_screen import SplashScreen  # Importa la pantalla de carga

# Importamos las páginas
from pages.home import Home
from pages.topics import Topics
from pages.projects import Projects
from app.window.pages.resource_manager import ResourceManager


class CustomButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setCheckable(True)  # Permite que el botón pueda quedarse en estado presionado
        self.setStyleSheet("""
            QPushButton {
                padding: 10px;
                border: none;
                color: #ae76ff;
                background-color: #1E1E1E;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(138, 43, 226, 0.5);  /* Gris-morado opaco al pasar el mouse */
            }
            QPushButton:checked {
                background-color: rgba(138, 43, 226, 0.5);  /* Gris-morado opaco cuando está seleccionado */
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación PyQt6 Modular")

        # Configuración para hacer la ventana a pantalla completa y sin botones
        self.setWindowState(Qt.WindowState.WindowFullScreen)  # Pantalla completa
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Deshabilitar bordes, minimizar, maximizar y cerrar

        # Configuración principal de la ventana
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Aplicamos la fuente global (Cascadia Code)
        font = QFont('Cascadia Code', 10)  # Usamos Cascadia Code
        QApplication.setFont(font)

        # Layout principal (horizontal: aside + espacio de contenido)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)  # Elimina márgenes
        main_layout.setSpacing(0)  # Elimina espacio entre widgets

        # Aside
        aside_layout = QVBoxLayout()
        aside_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)  # Centra el contenido verticalmente
        aside_layout.setContentsMargins(0, 0, 0, 0)  # Asegúrate de que no haya márgenes dentro del aside
        aside_widget = QWidget()
        aside_widget.setLayout(aside_layout)
        aside_widget.setFixedWidth(200)
        aside_widget.setStyleSheet("background-color: #1E1E1E; color: #53fc18;")

        # Botones del aside
        self.buttons = [
            CustomButton("Start"),
            CustomButton("Topics"),
            CustomButton("Projects"),
            CustomButton("Resources")
        ]

        for index, btn in enumerate(self.buttons):
            btn.clicked.connect(lambda _, i=index: self.change_page(i))  # Conectar botones a las páginas
            aside_layout.addWidget(btn)

        # Espacio principal (donde se renderizan las páginas)
        self.pages = QStackedWidget()
        self.pages.addWidget(Home())
        self.pages.addWidget(Topics())
        self.pages.addWidget(Projects())
        self.pages.addWidget(ResourceManager())

        # Añadimos aside y espacio principal al layout
        main_layout.addWidget(aside_widget)
        main_layout.addWidget(self.pages, stretch=1)

    def change_page(self, index):
        """Cambia la página en el QStackedWidget y actualiza el estado de los botones"""
        self.pages.setCurrentIndex(index)
        # Actualizar el estado de los botones
        for i, btn in enumerate(self.buttons):
            btn.setChecked(i == index)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Crear y mostrar la pantalla de carga
    splash = SplashScreen()

    # Crear la ventana principal
    window = MainWindow()

    # Conectar la señal de finalización de la pantalla de carga
    splash.finished.connect(window.show)

    # Mostrar la pantalla de carga
    splash.show()

    sys.exit(app.exec())
