from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class Projects(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        title = QLabel("Progreso de Proyectos")
        title.setStyleSheet("font-size: 20px; color: #2c3e50;")
        layout.addWidget(title)
        
        # Tabla de Proyectos
        table = QTableWidget(3, 3)
        table.setHorizontalHeaderLabels(["Proyecto", "Progreso", "Tiempo Total"])
        projects = [
            ("Proyecto 1", "80%", "5h 30m"),
            ("Proyecto 2", "50%", "2h"),
            ("Proyecto 3", "20%", "1h 10m"),
        ]
        
        for row, (name, progress, time) in enumerate(projects):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(progress))
            table.setItem(row, 2, QTableWidgetItem(time))
        
        layout.addWidget(table)
