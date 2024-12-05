from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

class CardInfo(QWidget):
    def __init__(self, project_name, activity_log):
        super().__init__()

        # Estilo para el card
        self.setStyleSheet("""
            QWidget {
                background-color: white;  /* Fondo blanco para el card */
                border-radius: 10px;
                margin-bottom: 10px;
                padding: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                max-width: 400px;
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
        project_name_label.setStyleSheet("background-color: #4CAF50; color: white; padding: 5px; border-radius: 5px;")
        name_layout.addWidget(project_name_label)
        layout.addWidget(name_container)

        # Contenedor para los detalles (fondo rojo)
        details_container = QWidget()
        details_layout = QVBoxLayout(details_container)
        details_label = QLabel("<b>Detalles</b>", self)
        details_label.setStyleSheet("background-color: #F44336; color: white; padding: 5px; border-radius: 5px;")
        details_layout.addWidget(details_label)

        # Añadir cada actividad al log de actividades (fondo amarillo)
        for entry in activity_log:
            activity_container = QWidget()
            activity_layout = QVBoxLayout(activity_container)
            
            activity_label = QLabel(f"{entry['date']}: {entry['activity']} - {entry['time_spent']} min", self)
            activity_label.setStyleSheet("background-color: #FFEB3B; padding: 5px; border-radius: 5px; margin: 2px 0;")
            activity_layout.addWidget(activity_label)
            details_layout.addWidget(activity_container)

        layout.addWidget(details_container)
