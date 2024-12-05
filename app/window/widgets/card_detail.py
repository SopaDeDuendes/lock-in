from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QFrame

class CardDetail(QWidget):
    def __init__(self, activity_log):
        super().__init__()

        # Crear el contenedor principal que será la "carta"
        card_container = QWidget(self)
        card_container.setStyleSheet("""
            QWidget {
                background-color: #d4f5d2;  /* Fondo verde claro */
                border-radius: 10px;
                padding: 15px;
                border: 2px solid #a8d5a2;  /* Borde más oscuro */
            }
        """)

        # Layout del contenedor principal
        card_layout = QVBoxLayout(card_container)
        card_layout.setSpacing(10)  # Espaciado entre elementos

        # Recorrer el log de actividades y crear los elementos
        for session in activity_log:
            # Crear y agregar la etiqueta de fecha
            date_label = QLabel(f"Fecha: {session['date']}")
            date_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            card_layout.addWidget(date_label)

            # Crear y agregar las etiquetas de tiempo (inicio, fin y duración)
            time_label = QLabel(f"Hora de inicio: {session['start_time']} - Hora de fin: {session['end_time']}")
            time_label.setStyleSheet("font-size: 12px;")
            card_layout.addWidget(time_label)

            duration_label = QLabel(f"Duración: {session['duration']} minutos")
            duration_label.setStyleSheet("font-size: 12px;")
            card_layout.addWidget(duration_label)

            # Layout para las tareas de la sesión
            task_layout = QVBoxLayout()
            for task in session['tasks']:
                task_checkbox = QCheckBox(task['task'])
                task_checkbox.setChecked(task['done'])  # Mostrar si está completada
                task_checkbox.setEnabled(False)  # Deshabilitar interacción
                task_layout.addWidget(task_checkbox)

            # Agregar el layout de tareas al layout de la tarjeta
            card_layout.addLayout(task_layout)

        # Layout principal de CardDetail
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(card_container)  # Agregar el contenedor completo
        self.layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes adicionales
