from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QSizePolicy, QStackedWidget, QScrollArea
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QCheckBox
from widgets.card_detail import CardDetail

class AnnualHeatmapWidget(QWidget):
    def __init__(self, sessions):
        super().__init__()
        self.sessions = sessions

        # Establecer un ancho máximo
        self.setMaximumWidth(630)  # Máximo de 650px
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        # Extraer todas las fechas únicas
        self.dates = set(session['date'] for session in sessions)

        # Atributos de fecha
        self.current_year = 2024

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(5)

        # Título del calendario anual
        title_label = QLabel(f"Calendario Anual {self.current_year}")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Calendario Anual (12 meses en cuadrícula 3x4)
        self.year_calendar = QWidget()
        year_calendar_layout = QGridLayout(self.year_calendar)
        year_calendar_layout.setContentsMargins(0, 0, 0, 0)
        year_calendar_layout.setSpacing(5)
        self.generate_annual_calendar(year_calendar_layout)

        # Área para mostrar los detalles del log de actividad
        self.detail_area = QStackedWidget()
        self.detail_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        # Agregar título, calendario y área de detalles al layout principal
        main_layout.addWidget(title_label)
        main_layout.addWidget(self.year_calendar)
        main_layout.addWidget(self.detail_area)

    def generate_annual_calendar(self, layout):
        """Genera el calendario anual con 12 meses en una cuadrícula 3x4."""
        months = [
            (1, "Enero"), (2, "Febrero"), (3, "Marzo"), (4, "Abril"),
            (5, "Mayo"), (6, "Junio"), (7, "Julio"), (8, "Agosto"),
            (9, "Septiembre"), (10, "Octubre"), (11, "Noviembre"), (12, "Diciembre")
        ]

        row, col = 0, 0
        for month_num, month_name in months:
            # Crear el widget para cada mes
            month_widget = self.create_month_widget(month_num, month_name)

            # Agregar el widget del mes en la cuadrícula
            layout.addWidget(month_widget, row, col)

            # Manejo de filas y columnas (3x4)
            col += 1
            if col == 4:  # Cambiar de fila después de 4 meses
                col = 0
                row += 1

    def create_month_widget(self, month_num, month_name):
        """Crea un widget para un mes específico."""
        # Establecer la fecha para el primer día del mes
        first_day_of_month = QDate(self.current_year, month_num, 1)
        days_in_month = first_day_of_month.daysInMonth()

        # Crear un widget para cada mes
        month_widget = QWidget()
        month_layout = QVBoxLayout(month_widget)
        month_layout.setSpacing(5)

        # Título del mes
        month_label = QLabel(month_name)
        month_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #bfc3cb;")
        month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Calendario del mes
        month_calendar = QWidget()
        month_calendar_layout = QGridLayout(month_calendar)
        month_calendar_layout.setContentsMargins(0, 0, 0, 0)
        month_calendar_layout.setSpacing(5)

        # Determinar el primer día de la semana del mes
        first_day_of_week = first_day_of_month.dayOfWeek()

        # Generar las celdas del mes
        self.generate_month_calendar(month_num, first_day_of_week, days_in_month, month_calendar_layout)

        # Agregar el título y el calendario al layout del mes
        month_layout.addWidget(month_label)
        month_layout.addWidget(month_calendar)

        # Asegurar que el mes se ajuste al contenedor
        month_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        return month_widget

    def generate_month_calendar(self, month_num, start_day, days_in_month, layout):
        """Genera las celdas de un mes específico."""
        row, col = 0, start_day - 1
        for day in range(1, days_in_month + 1):
            date_str = f"{self.current_year}-{month_num:02d}-{day:02d}"
            label = self.create_day_label(day, date_str)

            layout.addWidget(label, row, col)

            # Manejo de columnas y filas
            col += 1
            if col == 7:  # Nueva fila después de 7 días
                col = 0
                row += 1

    def create_day_label(self, day, date_str):
        """Crea una etiqueta para un día del mes."""
        label = QLabel(str(day))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedSize(15, 15)  # Tamaño compacto

        # Pintar de morado si la fecha está en las sesiones
        if date_str in self.dates:
            label.setStyleSheet("background-color: #ae76ff; color: white; border-radius: 5px;")
            label.mousePressEvent = lambda event, date=date_str: self.show_detail(date)  # Conectar clic
            # Cambiar el cursor al pointer cuando pase el ratón por encima
            label.setCursor(Qt.CursorShape.PointingHandCursor)
            # Evento de pasar el ratón sobre el día (hover)
            label.enterEvent = lambda event, label=label: label.setStyleSheet("""
                background-color: #D7BAF8;  
                color: white; 
                border-radius: 5px;
            """)
            # Evento de salir el ratón del día (resetear hover)
            label.leaveEvent = lambda event, label=label: label.setStyleSheet("""
                background-color: #ae76ff;  /* Color morado en estado normal */
                color: white; 
                border-radius: 5px;
            """)
        else:
            label.setStyleSheet("color: #989eab;")

        return label

    def show_detail(self, date):
        """Muestra los detalles de la actividad para la fecha seleccionada."""
        # Filtrar las sesiones por la fecha seleccionada
        activity_log = [session for session in self.sessions if session['date'] == date]
        
        # Instanciar y mostrar la clase CardDetail
        card_detail_widget = CardDetail(activity_log)
        
        # Agregar el widget de detalles a la área de detalles
        self.detail_area.addWidget(card_detail_widget)
        self.detail_area.setCurrentWidget(card_detail_widget)
