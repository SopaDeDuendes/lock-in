from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from widgets.card_info import CardInfo  # Asegúrate de importar correctamente la clase CardInfo

class Projects(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projects")
        
        layout = QVBoxLayout(self)

        # Scroll area for the projects list
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # Widget for holding all the cards
        projects_widget = QWidget()
        projects_layout = QVBoxLayout(projects_widget)
        scroll_area.setWidget(projects_widget)

        # Example predefined projects data
        projects_data = [
            {
                'name': 'Project 1',
                'activity_log': [
                    {'date': '2024-12-01', 'activity': 'Started project', 'time_spent': 120},
                    {'date': '2024-12-02', 'activity': 'Worked on feature A', 'time_spent': 90}
                ]
            },
            {
                'name': 'Project 2',
                'activity_log': [
                    {'date': '2024-12-01', 'activity': 'Research phase', 'time_spent': 60}
                ]
            },
            {
                'name': 'Project 1',
                'activity_log': [
                    {'date': '2024-12-01', 'activity': 'Started project', 'time_spent': 120},
                    {'date': '2024-12-02', 'activity': 'Worked on feature A', 'time_spent': 90}
                ]
            },
            {
                'name': 'Project 2',
                'activity_log': [
                    {'date': '2024-12-01', 'activity': 'Research phase', 'time_spent': 60}
                ]
            },
            {
                'name': 'Project 1',
                'activity_log': [
                    {'date': '2024-12-01', 'activity': 'Started project', 'time_spent': 120},
                    {'date': '2024-12-02', 'activity': 'Worked on feature A', 'time_spent': 90}
                ]
            },
            {
                'name': 'Project 2',
                'activity_log': [
                    {'date': '2024-12-01', 'activity': 'Research phase', 'time_spent': 60}
                ]
            }
        ]

        # Create a card for each project with predefined data
        for project in projects_data:
            card = CardInfo(project['name'], project['activity_log'])
            projects_layout.addWidget(card)
