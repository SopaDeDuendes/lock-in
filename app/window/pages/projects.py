from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from app.window.widgets.card_overview import CardOverview
from app.window.widgets.card_detail import CardDetail
from utils.json_manager import JsonManager
from widgets.heatmap_widget import HeatmapWidget

class Projects(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Projects")

        # Estilo general
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                color: #FFFFFF;
            }
            QScrollArea {
                background-color: #1E1E1E;
                border: none;
            }
            QLabel {
                color: #FFFFFF;
            }
        """)

        # Layout principal
        main_layout = QHBoxLayout(self)

        # Layout izquierdo
        left_layout = QVBoxLayout()
        self.projects_area = QWidget()
        self.projects_area.setLayout(left_layout)

        # Scroll area para el lado izquierdo
        left_scroll_area = QScrollArea(self)
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setWidget(self.projects_area)

        # Layout derecho (Aside para detalles)
        self.right_widget = QWidget()
        right_layout = QVBoxLayout(self.right_widget)
        self.logs_area = QWidget()
        self.logs_area.setLayout(QVBoxLayout())
        right_layout.addWidget(self.logs_area)

        # Scroll area para el aside
        self.right_scroll_area = QScrollArea(self)
        self.right_scroll_area.setWidgetResizable(True)
        self.right_scroll_area.setWidget(self.right_widget)

        # Agregar layouts al principal
        main_layout.addWidget(left_scroll_area)
        main_layout.addWidget(self.right_scroll_area)

        # Cargar datos de proyectos
        self.json_manager = JsonManager()
        self.projects_data = self.json_manager.read_json("projects")

        # Crear tarjetas de resumen y heatmaps
        self.cards = []
        for project in self.projects_data:
            self.add_project_to_layout(project, left_layout)

        # Ajustes de márgenes
        main_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setContentsMargins(0, 0, 0, 0)

    def add_project_to_layout(self, project, parent_layout):
        # Calcular tiempo total invertido
        total_time_spent = sum(session['duration'] for session in project['sessions'])

        # Contenedor para tarjeta y heatmap
        project_container = QWidget()
        project_layout = QVBoxLayout(project_container)
        project_layout.setContentsMargins(0, 0, 0, 20)

        # Crear la tarjeta de resumen
        card_overview = CardOverview(project['name'], total_time_spent)
        card_overview.setCursor(Qt.CursorShape.PointingHandCursor)
        card_overview.mousePressEvent = lambda event, p=project: self.show_project_logs(p)
        self.cards.append(card_overview)

        # Crear el heatmap
        heatmap_widget = HeatmapWidget(project['sessions'])

        # Agregar tarjeta y heatmap al contenedor
        project_layout.addWidget(card_overview)
        project_layout.addWidget(heatmap_widget)

        # Agregar el contenedor al layout padre
        parent_layout.addWidget(project_container)

    def show_project_logs(self, project):
        # Limpiar los logs actuales
        for i in range(self.logs_area.layout().count()):
            child = self.logs_area.layout().itemAt(i).widget()
            child.deleteLater()

        # Crear el título del proyecto seleccionado
        title_label = QLabel(project['name'])
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)

        # Crear el CardDetail con las sesiones del proyecto
        card_detail = CardDetail(project['sessions'])
        card_detail.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Agregar título y detalles al aside
        self.logs_area.layout().addWidget(title_label)
        self.logs_area.layout().addWidget(card_detail)

    def resizeEvent(self, event):
        # Mostrar u ocultar el aside según el ancho de la ventana
        if self.width() < 800:
            self.right_scroll_area.setVisible(False)
        else:
            self.right_scroll_area.setVisible(True)

        super().resizeEvent(event)