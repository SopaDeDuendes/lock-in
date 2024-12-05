from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from app.window.widgets.card_overview import CardOverview  # Importar CardOverview
from app.window.widgets.card_detail import CardDetail  # Importar CardDetail
from utils.json_manager import JsonManager  # Importar JsonManager


class Topics(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Topics")

        # Layout principal en H (Horizontal), para dividir la vista en dos partes
        main_layout = QHBoxLayout(self)

        # Layout izquierdo para los temas
        left_layout = QVBoxLayout()
        self.topics_area = QWidget()
        self.topics_area.setLayout(left_layout)  # Asignar layout al área de temas

        # Scroll area para el área de temas (lado izquierdo)
        left_scroll_area = QScrollArea(self)
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setWidget(self.topics_area)

        # Layout derecho para los logs del tema seleccionado
        right_widget = QWidget()  # Crear un widget para el lado derecho
        right_layout = QVBoxLayout(right_widget)
        self.logs_area = QWidget()  # Aquí se mostrarán los logs
        self.logs_area.setLayout(QVBoxLayout())  # Asignar un layout a logs_area
        right_layout.addWidget(self.logs_area)

        # Aplicar el estilo de fondo rojo al widget derecho
        right_widget.setStyleSheet("background-color: red;")

        # Scroll area para el área de logs (lado derecho)
        right_scroll_area = QScrollArea(self)
        right_scroll_area.setWidgetResizable(True)
        right_scroll_area.setWidget(right_widget)

        # Agregamos ambos layouts (izquierdo y derecho)
        main_layout.addWidget(left_scroll_area)  # Agregar el área de scroll izquierdo
        main_layout.addWidget(right_scroll_area)  # Agregar el área de scroll derecho

        # Inicializar JsonManager y cargar los datos
        self.json_manager = JsonManager()
        self.topics_data = self.json_manager.read_json("topics")  # Carga desde "data/topics.json"

        # Crear las tarjetas de resumen (CardOverview) y los detalles (CardDetail)
        self.cards = []
        for topic in self.topics_data:
            # Calcular el tiempo total invertido en el tema
            total_time_spent = sum(session['duration'] for session in topic['sessions'])

            # Crear la tarjeta de resumen (CardOverview)
            card_overview = CardOverview(topic['name'], total_time_spent)
            card_overview.mousePressEvent = lambda event, t=topic: self.show_topic_logs(t)  # Conectar clic al log
            self.cards.append(card_overview)
            left_layout.addWidget(card_overview)

        # Eliminar márgenes en el layout principal para evitar espacios innecesarios
        main_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes en el layout principal
        left_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes en el layout izquierdo
        right_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes en el layout derecho

    def show_topic_logs(self, topic):
        # Limpiar los logs actuales del aside
        for i in range(self.logs_area.layout().count()):
            child = self.logs_area.layout().itemAt(i).widget()
            child.deleteLater()

        # Crear el CardDetail para el tema seleccionado
        card_detail = CardDetail(topic['sessions'])
        self.logs_area.layout().addWidget(card_detail)
