from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt
from widgets.timer_dialog import TimerDialog  # Asegúrate de que la ruta es correcta

class Home(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Layout principal
        layout = QVBoxLayout(self)
        
        # Etiqueta que muestra el tiempo
        self.time_label = QLabel("00:00", self)
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        
        # Conectar el clic en la etiqueta del tiempo para abrir el diálogo
        self.time_label.setCursor(Qt.CursorShape.PointingHandCursor)  # Cambiar cursor al pasar sobre la etiqueta
        self.time_label.mousePressEvent = self.label_clicked
        
        # Agregar la etiqueta al layout
        layout.addWidget(self.time_label)
        
        self.setLayout(layout)

    def label_clicked(self, event):
        """Manejador para el clic en la etiqueta del tiempo."""
        dialog = TimerDialog(self, current_time=25)  # 25 es un ejemplo de tiempo inicial
        if dialog.exec():  # Solo actualiza si se presiona "Aceptar"
            nuevo_tiempo = dialog.get_time()
            self.update_time_label(nuevo_tiempo)

    def update_time_label(self, time_in_minutes):
        """Actualiza la etiqueta con el nuevo tiempo configurado."""
        self.time_label.setText(f"{time_in_minutes:02}:00")
