from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QWidget, QHBoxLayout, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Importamos las páginas
from pages.home import Home
from pages.topics import Topics
from pages.projects import Projects


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplicación PyQt6 Modular")
        self.setGeometry(100, 100, 800, 600)

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
        aside_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        aside_layout.setContentsMargins(0, 0, 0, 0)  # Asegúrate de que no haya márgenes dentro del aside
        aside_widget = QWidget()
        aside_widget.setLayout(aside_layout)
        aside_widget.setFixedWidth(200)
        aside_widget.setStyleSheet("background-color: #1E1E1E; color: #53fc18;")

        # Botones del aside
        btn_page1 = QPushButton("Start")
        btn_page2 = QPushButton("Topics")
        btn_page3 = QPushButton("Projects")

        for btn in [btn_page1, btn_page2, btn_page3]:
            btn.setStyleSheet("padding: 10px; border: none; color: #785fa0; background-color: #1E1E1E;")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            aside_layout.addWidget(btn)

        # Conexiones
        btn_page1.clicked.connect(lambda: self.change_page(0))
        btn_page2.clicked.connect(lambda: self.change_page(1))
        btn_page3.clicked.connect(lambda: self.change_page(2))

        # Espacio principal (donde se renderizan las páginas)
        self.pages = QStackedWidget()
        self.pages.addWidget(Home())
        self.pages.addWidget(Topics())
        self.pages.addWidget(Projects())

        # Añadimos aside y espacio principal al layout
        main_layout.addWidget(aside_widget)
        main_layout.addWidget(self.pages, stretch=1)

        # CSS global (opcional, puedes cargar desde un archivo)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E1E;
                color: #53fc18;
            }
            QPushButton:hover {
                background-color: #1abc9c;
            }
        """)

    def change_page(self, index):
        """Cambia la página en el QStackedWidget"""
        self.pages.setCurrentIndex(index)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
