from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QHBoxLayout
from PyQt6.QtCore import Qt, QSize

class CardDetail(QWidget):
    def __init__(self, activity_log):
        super().__init__()

        # Layout principal de CardDetail
        self.layout = QVBoxLayout(self)

        # Recorrer el log de actividades y crear los elementos
        for session in activity_log:
            # Crear un contenedor para cada carta con los estilos de fondo y borde
            card_container = QWidget(self)
            card_container.setStyleSheet("""
                QWidget {
                    background-color: #1E1E1E;  /* Fondo amarillo */
                    border-radius: 10px;
                    padding: 15px;
                    border: 2px solid #ae76ff;  /* Borde verde */
                }
            """)

            # Establecer un tamaño mínimo y máximo para las tarjetas
            card_container.setMinimumSize(QSize(200, 150))  # Tamaño mínimo
            # card_container.setMaximumSize(QSize(500, 300))  # Tamaño máximo

            # Layout del contenedor de cada carta
            card_layout = QVBoxLayout(card_container)
            card_layout.setSpacing(5)  # Reducir el espacio entre los elementos para hacerlo más compacto

            # Layout horizontal para mostrar fecha y tiempo total (en los extremos)
            date_time_layout = QHBoxLayout()

            # Etiqueta de la fecha
            date_label = QLabel(f"Fecha: {session['date']}")
            date_label.setStyleSheet("font-size: 16px; font-weight: bold;")  # Reducir tamaño de la fuente
            date_time_layout.addWidget(date_label)

            # Etiqueta del tiempo total
            total_time_label = QLabel(f"Tiempo total: {session['duration']} minutos")
            total_time_label.setStyleSheet("font-size: 14px;")  # Reducir tamaño de la fuente
            date_time_layout.addWidget(total_time_label, alignment=Qt.AlignmentFlag.AlignRight)

            # Agregar el layout de fecha y tiempo total al layout principal
            card_layout.addLayout(date_time_layout)

            # Rango de horas (hora de inicio y fin)
            time_label = QLabel(f"De {session['start_time']} a {session['end_time']}")
            time_label.setStyleSheet("font-size: 12px;")  # Mantener el tamaño pequeño
            card_layout.addWidget(time_label)

            # Layout para las tareas de la sesión
            task_layout = QVBoxLayout()
            for task in session['tasks']:
                task_checkbox = QCheckBox(task['task'])
                task_checkbox.setChecked(task['done'])  # Mostrar si está completada
                task_checkbox.setEnabled(False)  # Deshabilitar interacción
                task_checkbox.setStyleSheet("font-size: 12px;")  # Reducir tamaño de fuente de las tareas
                task_layout.addWidget(task_checkbox)

            # Agregar el layout de tareas al layout de la tarjeta
            card_layout.addLayout(task_layout)

            # Agregar el contenedor de la carta al layout principal
            self.layout.addWidget(card_container)

        # Eliminar márgenes adicionales en el layout
        self.layout.setContentsMargins(0, 0, 0, 0)  # Eliminar márgenes del layout principal

        # Hacer que las tarjetas se ajusten si hay más de 2
        self.layout.setSpacing(10)  # Espacio entre las tarjetas
        self.layout.addStretch(1)  # Añadir espacio flexible al final
