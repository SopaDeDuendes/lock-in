from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea,QSizePolicy
from PyQt6.QtCore import Qt

from app.window.widgets.card_overview import CardOverview  # Importar CardOverview
from app.window.widgets.card_detail import CardDetail  # Importar CardDetail
from utils.json_manager import JsonManager  # Importar JsonManager


class Projects(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projects")

        # Layout principal en H (Horizontal), para dividir la vista en dos partes
        main_layout = QHBoxLayout(self)

        # Layout izquierdo para los proyectos
        left_layout = QVBoxLayout()
        self.projects_area = QWidget()
        self.projects_area.setLayout(left_layout)  # Asignar layout al área de proyectos

        # Scroll area para el área de proyectos (lado izquierdo)
        left_scroll_area = QScrollArea(self)
        left_scroll_area.setWidgetResizable(True)
        left_scroll_area.setWidget(self.projects_area)

        # Layout derecho para los logs del proyecto seleccionado
        self.right_widget = QWidget()  # Crear un widget para el lado derecho
        right_layout = QVBoxLayout(self.right_widget)
        self.logs_area = QWidget()  # Aquí se mostrarán los logs
        self.logs_area.setLayout(QVBoxLayout())  # Asignar un layout a logs_area
        right_layout.addWidget(self.logs_area)

        # Scroll area para el área de logs (lado derecho)
        self.right_scroll_area = QScrollArea(self)
        self.right_scroll_area.setWidgetResizable(True)
        self.right_scroll_area.setWidget(self.right_widget)

        # Agregamos ambos layouts (izquierdo y derecho)
        main_layout.addWidget(left_scroll_area)  # Agregar el área de scroll izquierdo
        main_layout.addWidget(self.right_scroll_area)  # Agregar el área de scroll derecho

        # Inicializar JsonManager y cargar los datos
        self.json_manager = JsonManager()
        self.projects_data = self.json_manager.read_json("projects")  # Carga desde "data/projects.json"

        # Crear las tarjetas de resumen (CardOverview) y los detalles (CardDetail)
        self.cards = []
        for project in self.projects_data:
            # Calcular el tiempo total invertido en el proyecto
            total_time_spent = sum(session['duration'] for session in project['sessions'])

            # Crear la tarjeta de resumen (CardOverview)
            card_overview = CardOverview(project['name'], total_time_spent)
            card_overview.mousePressEvent = lambda event, p=project: self.show_project_logs(p)  # Conectar clic al log
            self.cards.append(card_overview)
            left_layout.addWidget(card_overview)

        # Eliminar márgenes en el layout principal para evitar espacios innecesarios
        main_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes en el layout principal
        left_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes en el layout izquierdo
        right_layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes en el layout derecho

    def show_project_logs(self, project):
        # Limpiar los logs actuales del aside
        for i in range(self.logs_area.layout().count()):
            child = self.logs_area.layout().itemAt(i).widget()
            child.deleteLater()

        # Crear el CardDetail para el proyecto seleccionado
        card_detail = CardDetail(project['sessions'])

        # Ajustamos el ancho de card_detail para que no exceda el ancho del aside
        max_width = self.projects_area.width()  # Obtener el ancho disponible en el área de proyectos
        card_detail.setMaximumWidth(max_width)  # Limitar el ancho del widget de detalles al ancho disponible

        # Asegurar que no se muestre el desplazamiento horizontal
        card_detail.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)  # Expande solo horizontalmente

        self.logs_area.layout().addWidget(card_detail)

    def resizeEvent(self, event):
        # Obtenemos el ancho de la ventana
        window_width = self.width()

        # Si el ancho de la ventana es menor que 800px, ocultamos el aside
        if window_width < 800:
            self.right_scroll_area.setVisible(False)  # Ocultar el aside
        else:
            self.right_scroll_area.setVisible(True)  # Mostrar el aside

        # Llamar al método base resizeEvent para asegurarnos de que el evento se maneje correctamente
        super().resizeEvent(event)
