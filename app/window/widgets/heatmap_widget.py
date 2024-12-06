from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QGridLayout, QPushButton
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QColor, QPainter

class HeatmapWidget(QWidget):
    def __init__(self, sessions):
        super().__init__()
        self.sessions = sessions

        # Extraer todas las fechas únicas
        self.dates = set(session['date'] for session in sessions)

        # Atributos de fecha
        self.current_date = QDate(2024, 1, 1)  # Comenzamos con enero de 2024

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Título del calendario y controles
        title_layout = QHBoxLayout()
        self.title_label = QLabel(self.get_month_name(self.current_date))
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Botones de navegación
        prev_button = QPushButton("< Anterior")
        next_button = QPushButton("Siguiente >")

        prev_button.clicked.connect(self.previous_month)
        next_button.clicked.connect(self.next_month)

        title_layout.addWidget(prev_button)
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(next_button)

        # Calendario (matriz de fechas)
        self.calendar = QWidget()
        self.calendar_layout = QGridLayout(self.calendar)
        self.calendar_layout.setContentsMargins(0, 0, 0, 0)
        self.calendar_layout.setSpacing(5)

        # Generar el calendario
        self.generate_calendar()

        # Agregar al layout principal
        main_layout.addLayout(title_layout)
        main_layout.addWidget(self.calendar)

    def generate_calendar(self):
        """Genera el calendario para el mes actual."""
        # Limpiar el calendario actual
        for i in range(self.calendar_layout.count()):
            item = self.calendar_layout.itemAt(i)
            if item is not None:
                item.widget().deleteLater()

        # Obtener los días del mes actual
        days_in_month = self.current_date.daysInMonth()
        first_day_of_month = self.current_date.addDays(-self.current_date.day() + 1).dayOfWeek()
        
        row, col = 0, first_day_of_month - 1
        for day in range(1, days_in_month + 1):
            date_str = f"{self.current_date.year()}-{self.current_date.month():02d}-{day:02d}"
            label = QLabel(str(day))
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setFixedSize(30, 30)  # Celdas más pequeñas

            # Pintar de morado si la fecha está en las sesiones
            if date_str in self.dates:
                label.setStyleSheet("background-color: #8A2BE2; color: white; border-radius: 5px;")
            else:
                label.setStyleSheet("color: white;")

            self.calendar_layout.addWidget(label, row, col)

            # Manejo de columnas y filas
            col += 1
            if col == 7:  # Nueva fila
                col = 0
                row += 1

    def previous_month(self):
        """Navega al mes anterior."""
        self.current_date = self.current_date.addMonths(-1)
        self.update_calendar()

    def next_month(self):
        """Navega al mes siguiente."""
        self.current_date = self.current_date.addMonths(1)
        self.update_calendar()

    def update_calendar(self):
        """Actualiza el título y el calendario con el mes actual."""
        self.title_label.setText(self.get_month_name(self.current_date))
        self.generate_calendar()

    def get_month_name(self, date):
        """Devuelve el nombre del mes para la fecha dada."""
        return date.toString("MMMM yyyy")
