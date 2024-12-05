from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame
from widgets.card_overview import CardOverview  # Importar CardOverview
from widgets.card_detail import CardDetail  # Importar CardDetail

class Projects(QWidget):
    # def __init__(self):
        super().__init__()

        self.setWindowTitle("Projects")
        
        # Layout principal en H (Horizontal), para dividir la vista en dos partes
        main_layout = QHBoxLayout(self)

        # Layout izquierdo para los proyectos
        left_layout = QVBoxLayout()
        self.projects_area = QWidget()
        left_layout.addWidget(self.projects_area)

        # Scroll area para los proyectos
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.projects_area)

        # Layout derecho para los logs del proyecto seleccionado
        right_layout = QVBoxLayout()
        self.logs_area = QWidget()  # Aquí se mostrarán los logs
        right_layout.addWidget(self.logs_area)
        
        # Apartado de aside (con color rojo de fondo)
        aside_frame = QFrame(self)
        aside_frame.setStyleSheet("background-color: red;")
        aside_frame.setLayout(right_layout)

        # Agregamos ambos layouts (izquierdo y derecho)
        main_layout.addLayout(left_layout)
        main_layout.addWidget(aside_frame)

        # Datos de ejemplo para los proyectos
        projects_data = [
            {
                'name': 'Project 1',
                'activity_log': [
                    {'date': '2024-12-01', 'time_spent': 120, 'tasks': [
                        {'task': 'Task A', 'completed': True},
                        {'task': 'Task B', 'completed': False},
                    ]},
                    {'date': '2024-12-02', 'time_spent': 90, 'tasks': [
                        {'task': 'Task C', 'completed': True},
                        {'task': 'Task D', 'completed': True},
                    ]}
                ]
            },
            {
                'name': 'Project 2',
                'activity_log': [
                    {'date': '2024-12-01', 'time_spent': 60, 'tasks': [
                        {'task': 'Research Phase', 'completed': True}
                    ]}
                ]
            },
        ]

        # Crear las tarjetas de resumen (CardOverview) y los detalles (CardDetail)
        self.cards = []
        for project in projects_data:
            # Calcular el tiempo total invertido en el proyecto
            total_time_spent = sum(log['time_spent'] for log in project['activity_log'])

            # Crear la tarjeta de resumen (CardOverview)
            card_overview = CardOverview(project['name'], total_time_spent)
            card_overview.mousePressEvent = lambda event, p=project: self.show_project_logs(p)  # Conectar clic al log
            self.cards.append(card_overview)
            left_layout.addWidget(card_overview)

    def show_project_logs(self, project):
        # Limpiar los logs actuales del aside
        for i in range(self.logs_area.layout().count()):
            child = self.logs_area.layout().itemAt(i).widget()
            child.deleteLater()

        # Crear el CardDetail para el proyecto seleccionado
        card_detail = CardDetail(project['activity_log'])
        self.logs_area.layout().addWidget(card_detail)
