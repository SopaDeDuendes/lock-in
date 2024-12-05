import sys
import os
import json
import shutil
import webbrowser
import fitz  # PyMuPDF
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLineEdit, QLabel, QGridLayout, QScrollArea, QFrame, QHBoxLayout, QSizePolicy, QSplitter
import requests
from bs4 import BeautifulSoup

# Ruta al escritorio y crear la carpeta resources
def get_desktop_path():
    if sys.platform == "win32":
        return os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    elif sys.platform == "darwin":
        return os.path.join(os.path.expanduser('~'), 'Desktop')
    else:
        return os.path.join(os.path.expanduser('~'), 'Desktop')

def create_resources_folder():
    desktop_path = get_desktop_path()
    resources_folder = os.path.join(desktop_path, "resources")
    if not os.path.exists(resources_folder):
        os.makedirs(resources_folder)
    return resources_folder

def get_page_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else "Sin título"
        return title
    except requests.exceptions.RequestException:
        return "Error al cargar la página"

class ResourceCard(QFrame):
    def __init__(self, resource_type, resource_data, callback, title=None):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)

        self.resource_type = resource_type
        self.resource_data = resource_data
        self.callback = callback  # Callback para mostrar la previsualización
        self.title = title  # Título del recurso (para enlaces)

        layout = QHBoxLayout()  # Usamos un QHBoxLayout para todo en horizontal

        # Etiqueta para mostrar el nombre del recurso
        if self.resource_type == "pdf":
            name_label = QLabel(os.path.basename(resource_data))  # Nombre real del PDF
        elif self.resource_type == "link":
            name_label = QLabel(self.title)  # Título del enlace

        layout.addWidget(name_label)

        self.setLayout(layout)

        # Conectar el clic de la carta para mostrar el preview
        self.mousePressEvent = lambda event: self.callback(self)

    def view_resource(self):
        # Función para ver el recurso (puedes definir la lógica aquí)
        print(f"Ver: {self.resource_data}")

    def edit_resource(self):
        # Función para editar el recurso (puedes definir la lógica aquí)
        print(f"Editar: {self.resource_data}")

    def delete_resource(self):
        # Función para eliminar el recurso (puedes definir la lógica aquí)
        print(f"Eliminar: {self.resource_data}")

class ResourceManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Biblioteca de Recursos")

        main_layout = QHBoxLayout()

        # Crear el panel de recursos
        self.resource_layout = QVBoxLayout()

        # Crear el splitter para separar el listado y el preview
        splitter = QSplitter(Qt.Orientation.Horizontal)

        # Crear el área de scroll para los recursos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.create_resource_container())
        
        splitter.addWidget(scroll_area)

        # Crear el panel de previsualización (aside)
        self.preview_panel = QWidget()
        self.preview_layout = QVBoxLayout()
        self.preview_panel.setLayout(self.preview_layout)
        
        # Limitar el ancho del panel de previsualización
        self.preview_panel.setMaximumWidth(400)

        splitter.addWidget(self.preview_panel)

        # Añadir el splitter al layout principal
        main_layout.addWidget(splitter)

        self.setLayout(main_layout)

        # Ruta al archivo JSON donde se almacenarán los recursos
        self.resources_json_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "resources.json")
        self.load_resources()

    def create_resource_container(self):
        container = QWidget()
        container.setLayout(self.resource_layout)  # Usamos el layout vertical para apilar las filas
        return container

    def add_resource(self):
        file_dialog = QFileDialog(self)
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFiles)
        file_dialog.setNameFilter("PDF Files (*.pdf);;All Files (*)")

        if file_dialog.exec():
            files = file_dialog.selectedFiles()
            for file in files:
                # Copiar el archivo PDF a la carpeta 'resources'
                resources_folder = create_resources_folder()
                file_name = os.path.basename(file)
                destination = os.path.join(resources_folder, file_name)
                shutil.copy(file, destination)  # Copiar archivo a la carpeta de recursos

                # Guardamos la ruta del archivo copiado en el JSON
                self.save_resource("pdf", destination)
                resource_card = ResourceCard("pdf", destination, self.show_preview)
                self.add_to_layout(resource_card)

    def add_to_layout(self, card):
        self.resource_layout.addWidget(card)

    def save_resource(self, resource_type, resource_data):
        # Cargar los recursos actuales desde el archivo JSON
        if os.path.exists(self.resources_json_path):
            with open(self.resources_json_path, 'r') as f:
                resources = json.load(f)
        else:
            resources = {"pdf": [], "link": []}

        # Agregar el nuevo recurso a la lista
        if resource_type == "pdf":
            resources["pdf"].append(resource_data)
        elif resource_type == "link":
            title = get_page_title(resource_data)
            resources["link"].append({"url": resource_data, "title": title})

        # Guardar los recursos actualizados en el archivo JSON
        with open(self.resources_json_path, 'w') as f:
            json.dump(resources, f, indent=4)

    def load_resources(self):
        # Cargar recursos desde el archivo JSON al inicio
        if os.path.exists(self.resources_json_path):
            with open(self.resources_json_path, 'r') as f:
                resources = json.load(f)

            for pdf in resources.get("pdf", []):
                resource_card = ResourceCard("pdf", pdf, self.show_preview)
                self.add_to_layout(resource_card)

            for link in resources.get("link", []):
                resource_card = ResourceCard("link", link["url"], self.show_preview, title=link["title"])
                self.add_to_layout(resource_card)

    def show_preview(self, resource_card):
        # Limpiar el layout de la vista previa
        while self.preview_layout.count():
            item = self.preview_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if resource_card.resource_type == "pdf":
            # Mostrar la vista previa de PDF
            self.show_pdf_preview(resource_card.resource_data)
        elif resource_card.resource_type == "link":
            # Mostrar la vista previa del enlace
            self.show_link_preview(resource_card.resource_data)

    def show_pdf_preview(self, pdf_path):
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)
        pix = page.get_pixmap()
        preview_pixmap = QPixmap.fromImage(QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888))

        # Redimensionar la imagen del PDF para que ocupe menos espacio
        preview_pixmap = preview_pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
        self.preview_layout.addWidget(QLabel("Vista previa del PDF:"))
        self.preview_layout.addWidget(QLabel("Aquí se muestra la primera página"))
        self.preview_layout.addWidget(QLabel(f"Ruta: {pdf_path}"))
        preview_label = QLabel()
        preview_label.setPixmap(preview_pixmap)
        self.preview_layout.addWidget(preview_label)

    def show_link_preview(self, link):
        title = get_page_title(link)
        self.preview_layout.addWidget(QLabel(f"Vista previa del enlace: {link}"))
        self.preview_layout.addWidget(QLabel(f"Título: {title}"))

        # Mostrar la imagen del link
        link_image = QPixmap("app/window/assets/link.svg")
        link_image_label = QLabel()
        link_image_label.setPixmap(link_image)
        self.preview_layout.addWidget(link_image_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ResourceManager()
    window.show()
    sys.exit(app.exec())