from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox
from PyQt6.QtCore import Qt

class CardInfo(QWidget):
    def __init__(self, project_name, activity_log):
        super().__init__()

        # Estilo para el card
        self.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;  /* Fondo blanco para el card */
                border-radius: 10px;
                margin-bottom: 10px;
                padding: 10px;
                max-width: 600px;
                border: 2px solid #333333;
            }
            QLabel {
                color: #333;
            }
            .header {
                background-color: #4CAF50;  /* Fondo verde para el encabezado */
                padding: 5px;
                border-radius: 5px;
                color: white;
            }
            .details {
                background-color: #F44336;  /* Fondo rojo para los detalles */
                padding: 5px;
                border-radius: 5px;
                color: white;
            }
            .activity {
                background-color: #FFEB3B; /* Fondo amarillo para cada actividad */
                padding: 5px;
                border-radius: 5px;
                margin: 2px 0;
            }
        """)

        layout = QVBoxLayout(self)
        
        # Contenedor para el nombre del proyecto (fondo verde)
        name_container = QWidget()
        name_layout = QHBoxLayout(name_container)
        project_name_label = QLabel(f"<b>{project_name}</b>", self)
        project_name_label.setStyleSheet("background-color: #1E1E1E; color: #785fa0; padding: 5px; border-radius: 5px; font-size: 24px;")
        name_layout.addWidget(project_name_label)
        layout.addWidget(name_container)

        # Contenedor para los detalles (fondo rojo)
        details_container = QWidget()
        details_layout = QVBoxLayout(details_container)
        details_label = QLabel("<b>Detalles</b>", self)
        details_label.setStyleSheet("background-color: #1E1E1E; color: white; padding: 5px; border-radius: 5px; font-weight: bold;")
        details_layout.addWidget(details_label)

        # Añadir las instancias de actividad (fechas y tareas) dentro de los detalles
        for entry in activity_log:
            activity_container = QWidget()
            activity_layout = QVBoxLayout(activity_container)
            
            # Mostrar fecha y tiempo de la sesión
            session_info = QLabel(f"{entry['date']} - {entry['time_spent']} min", self)
            session_info.setStyleSheet("background-color: #1E1E1E; padding: 5px; border-radius: 5px; color: white;")
            activity_layout.addWidget(session_info)
            
            # Mostrar tareas realizadas en esa fecha
            for task in entry['tasks']:
                task_checkbox = QCheckBox(task['task'], self)
                task_checkbox.setChecked(task['completed'])  # Solo lectura, no se puede modificar
                task_checkbox.setDisabled(True)  # Deshabilitado para impedir edición
                activity_layout.addWidget(task_checkbox)

            details_layout.addWidget(activity_container)

        layout.addWidget(details_container)
