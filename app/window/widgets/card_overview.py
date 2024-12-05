from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CardOverview(QWidget):
    def __init__(self, project_name, total_time_spent):
        super().__init__()

        layout = QVBoxLayout(self)

        # Nombre del proyecto en grande
        self.project_name_label = QLabel(project_name, self)
        self.project_name_label.setStyleSheet("font-size: 20px; font-weight: bold; background-color: red;")

        # Tiempo total invertido en el proyecto
        self.total_time_label = QLabel(f"Total Time: {total_time_spent} mins", self)
        self.total_time_label.setStyleSheet("font-size: 18px; color: gray;background-color: red;")

        layout.addWidget(self.project_name_label)
        layout.addWidget(self.total_time_label)

        self.setLayout(layout)
