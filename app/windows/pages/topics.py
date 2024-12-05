from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QFrame
from widgets.card_overview import CardOverview  # Importar CardOverview
from widgets.card_detail import CardDetail  # Importar CardDetail

class Topics(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Topics")

        # Layout principal en H (Horizontal), para dividir la vista en dos partes
        main_layout = QHBoxLayout(self)

        # Layout izquierdo para los temas
        left_layout = QVBoxLayout()
        self.topics_area = QWidget()
        left_layout.addWidget(self.topics_area)

        # Scroll area para los temas
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.topics_area)

        # Layout derecho para los logs del tema seleccionado
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

        # Datos de ejemplo para los temas
        topics_data = [
            {
                'name': 'Mathematics',
                'activity_log': [
                    {'date': '2024-12-01', 'time_spent': 120, 'tasks': [
                        {'task': 'Review Calculus', 'completed': True},
                        {'task': 'Linear Algebra Practice', 'completed': False},
                    ]},
                    {'date': '2024-12-02', 'time_spent': 90, 'tasks': [
                        {'task': 'Differential Equations', 'completed': True},
                        {'task': 'Probability Theory', 'completed': False},
                    ]}
                ]
            },
            {
                'name': 'Physics',
                'activity_log': [
                    {'date': '2024-12-01', 'time_spent': 60, 'tasks': [
                        {'task': 'Quantum Mechanics', 'completed': True}
                    ]}
                ]
            },
            {
                'name': 'Computer Science',
                'activity_log': [
                    {'date': '2024-12-03', 'time_spent': 150, 'tasks': [
                        {'task': 'Algorithms and Data Structures', 'completed': False},
                        {'task': 'Introduction to Machine Learning', 'completed': True},
                    ]}
                ]
            },
            {
                'name': 'Neuroscience',
                'activity_log': [
                    {'date': '2024-12-02', 'time_spent': 120, 'tasks': [
                        {'task': 'Brain Anatomy', 'completed': True},
                        {'task': 'Neurobiology', 'completed': False},
                    ]}
                ]
            }
        ]

        # Crear las tarjetas de resumen (CardOverview) y los detalles (CardDetail)
        self.cards = []
        for topic in topics_data:
            # Calcular el tiempo total invertido en el tema
            total_time_spent = sum(log['time_spent'] for log in topic['activity_log'])

            # Crear la tarjeta de resumen (CardOverview)
            card_overview = CardOverview(topic['name'], total_time_spent)
            card_overview.mousePressEvent = lambda event, t=topic: self.show_topic_logs(t)  # Conectar clic al log
            self.cards.append(card_overview)
            left_layout.addWidget(card_overview)

    def show_topic_logs(self, topic):
        # Limpiar los logs actuales del aside
        for i in range(self.logs_area.layout().count()):
            child = self.logs_area.layout().itemAt(i).widget()
            child.deleteLater()

        # Crear el CardDetail para el tema seleccionado
        card_detail = CardDetail(topic['activity_log'])
        self.logs_area.layout().addWidget(card_detail)
