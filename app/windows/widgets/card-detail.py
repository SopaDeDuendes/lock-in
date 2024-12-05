from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class CardDetail(QWidget):
    def __init__(self, activity_log):
        super().__init__()

        layout = QVBoxLayout(self)

        # Recorrer y mostrar los logs de actividad (fecha y tareas)
        for log in activity_log:
            log_entry = QLabel(f"Date: {log['date']} - Time Spent: {log['time_spent']} mins", self)
            layout.addWidget(log_entry)
            for task in log['tasks']:
                task_label = QLabel(f"  Task: {task['task']} - Completed: {'Yes' if task['completed'] else 'No'}", self)
                layout.addWidget(task_label)

        self.setLayout(layout)
