from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from widgets.card_info import CardInfo  # Importa la clase CardInfo

class Topics(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Topics")

        layout = QVBoxLayout(self)

        # Scroll area for the topics list
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Widget for holding all the cards
        topics_widget = QWidget()
        topics_layout = QVBoxLayout(topics_widget)
        scroll_area.setWidget(topics_widget)

        # Example predefined topics data
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

        # Create a card for each topic with predefined data
        for topic in topics_data:
            card = CardInfo(topic['name'], topic['activity_log'])
            topics_layout.addWidget(card)
