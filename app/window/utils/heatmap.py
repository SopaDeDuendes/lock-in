import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QFrame
from PyQt6.QtCore import Qt

class AnnualHeatmapWidget(QWidget):
    def __init__(self, data, year=2024):
        super().__init__()
        self.data = data
        self.year = year
        self.setWindowTitle(f"Heatmap Anual - {year}")
        self.setGeometry(100, 100, 1200, 700)

        # Crear la interfaz gráfica
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)

        self.display_heatmap()

    def display_heatmap(self):
        # Días de la semana
        days_of_week = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]

        # Agregar etiquetas de los días de la semana (filas)
        for i, day in enumerate(days_of_week):
            label = QLabel(day)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(label, i + 1, 0)

        # Agregar los nombres de los meses en la fila superior
        months = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        for i, month in enumerate(months):
            label = QLabel(month)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.layout.addWidget(label, 0, i + 1)

        # Crear un marco de 7 filas y 12 columnas para los días y meses
        week_of_year = 52
        days_in_week = 7

        # Iterar sobre las semanas y días
        for week in range(week_of_year):
            for day in range(days_in_week):
                frame = QFrame(self)
                frame.setFrameShape(QFrame.Shape.StyledPanel)  # Cambio aquí

                # Calcular el día del año
                day_of_year = week * days_in_week + day + 1

                # Verificar si hubo actividad en ese día
                if self.is_study_day(day_of_year):
                    frame.setStyleSheet("background-color: green;")
                else:
                    frame.setStyleSheet("background-color: white;")

                # Ajustar el tamaño de las celdas a 15x15 px
                frame.setFixedSize(15, 15)
                self.layout.addWidget(frame, day + 1, (week % 12) + 1)  # Colocar en la columna correspondiente

    def is_study_day(self, day_of_year):
        """
        Determina si hubo actividad en este día del año.
        """
        # Calcular la fecha del día del año (1 a 365)
        day_of_month = day_of_year
        month, day = self.get_month_and_day(day_of_month)
        date_str = f"{self.year}-{month:02d}-{day:02d}"

        # Verificar si este día tiene actividad en las sesiones
        for project in self.data:
            for session in project['sessions']:
                if session['date'] == date_str:
                    return True
        return False

    def get_month_and_day(self, day_of_year):
        """
        Convierte el día del año (1-365) a mes y día del mes.
        """
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if (self.year % 4 == 0 and self.year % 100 != 0) or (self.year % 400 == 0):
            days_in_month[1] = 29  # Ajustar para los años bisiestos

        month = 1
        while day_of_year > days_in_month[month - 1]:
            day_of_year -= days_in_month[month - 1]
            month += 1

        return month, day_of_year

# Crear la aplicación y la ventana
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Datos de ejemplo
    data = [
        {"name": "Matemáticas", "sessions": [{"date": "2024-01-05", "duration": 60}, {"date": "2024-03-15", "duration": 45}]},
        {"name": "Física", "sessions": [{"date": "2024-01-10", "duration": 120}, {"date": "2024-12-20", "duration": 90}]},
        {"name": "Biología", "sessions": [{"date": "2024-02-03", "duration": 75}, {"date": "2024-09-08", "duration": 30}]}
    ]

    # Instanciamos el widget del heatmap
    heatmap_widget = AnnualHeatmapWidget(data, year=2024)
    heatmap_widget.show()

    sys.exit(app.exec())  # Usar exec() en lugar de exec_()
