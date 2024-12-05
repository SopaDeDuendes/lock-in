from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np

class Topics(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        title = QLabel("Mapa de Calor del Tiempo")
        title.setStyleSheet("font-size: 20px; color: #a36fc3;")
        layout.addWidget(title)
        
        # Generar Heatmap
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        
        data = np.random.rand(7, 24)  # Datos de ejemplo
        heatmap = ax.imshow(data, cmap="coolwarm", aspect="auto")
        figure.colorbar(heatmap)
        
        layout.addWidget(canvas)
