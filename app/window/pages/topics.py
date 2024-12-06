from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QSizePolicy, QLabel
)
from PyQt6.QtCore import Qt
from app.window.widgets.card_overview import CardOverview
from app.window.widgets.card_detail import CardDetail
from utils.json_manager import JsonManager
from widgets.annual_heatmap_widget import AnnualHeatmapWidget

class Topics(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Topics")

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
        self.topics_area = QWidget()
        self.topics_area.setLayout(left_layout)

        # Scroll area para el lado izquierdo
        left_scroll_area = QScrollArea(self)
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setWidget(self.topics_area)

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

        # Cargar datos de temas
        self.json_manager = JsonManager()
        self.topics_data = self.json_manager.read_json("topics")

        # Crear tarjetas de resumen y heatmaps
        self.cards = []
        for topic in self.topics_data:
            self.add_topic_to_layout(topic, left_layout)

        # Ajustes de márgenes
        main_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setContentsMargins(10, 10, 10, 10)
        right_layout.setContentsMargins(0, 0, 0, 0)

    def add_topic_to_layout(self, topic, parent_layout):
        # Calcular tiempo total invertido
        total_time_spent = sum(session['duration'] for session in topic['sessions'])

        # Contenedor para tarjeta y heatmap
        topic_container = QWidget()
        topic_layout = QVBoxLayout(topic_container)
        topic_layout.setContentsMargins(0, 0, 0, 20)

        # Crear la tarjeta de resumen
        card_overview = CardOverview(topic['name'], total_time_spent)
        card_overview.setCursor(Qt.CursorShape.PointingHandCursor)
        card_overview.mousePressEvent = lambda event, t=topic: self.show_topic_logs(t)
        self.cards.append(card_overview)

        # Agregar tarjeta y heatmap al contenedor
        topic_layout.addWidget(card_overview)

        # Agregar el contenedor al layout padre
        parent_layout.addWidget(topic_container)

    def show_topic_logs(self, topic):
        # Limpiar los logs actuales
        for i in range(self.logs_area.layout().count()):
            child = self.logs_area.layout().itemAt(i).widget()
            child.deleteLater()

        # Crear el título del tema seleccionado
        title_label = QLabel(topic['name'])
        title_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setWordWrap(True)

        # # Crear el CardDetail con las sesiones del tema
        # card_detail = CardDetail(topic['sessions'])
        # card_detail.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Crear el calendario anual y pasarlo al contenedor
        annual_calendar_widget = AnnualHeatmapWidget(topic['sessions'])
        annual_calendar_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Agregar título, detalles y calendario al aside
        self.logs_area.layout().addWidget(title_label)
        self.logs_area.layout().addWidget(annual_calendar_widget)
        # self.logs_area.layout().addWidget(card_detail)

    def resizeEvent(self, event):
        # Mostrar u ocultar el aside según el ancho de la ventana
        if self.width() < 800:
            self.right_scroll_area.setVisible(False)
        else:
            self.right_scroll_area.setVisible(True)

        super().resizeEvent(event)
