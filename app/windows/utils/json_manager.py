import json
import os
from typing import List, Dict, Any, Optional

class JsonManager:
    def __init__(self, base_folder: str = "data"):
        """
        Inicializa el administrador de JSON con una carpeta base.
        """
        self.base_folder = base_folder
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)

    def _get_file_path(self, folder: str, file_name: str) -> str:
        """
        Obtiene la ruta completa del archivo JSON.
        """
        dir_path = os.path.join(self.base_folder, folder)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return os.path.join(dir_path, f"{file_name}.json")

    def read_json(self, folder: str, file_name: str) -> Optional[Dict[str, Any]]:
        """
        Lee un archivo JSON y devuelve su contenido.
        """
        file_path = self._get_file_path(folder, file_name)
        if not os.path.exists(file_path):
            return None
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write_json(self, folder: str, file_name: str, data: Dict[str, Any]) -> bool:
        """
        Escribe un diccionario en un archivo JSON.
        """
        file_path = self._get_file_path(folder, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True

    def list_files(self, folder: str) -> List[str]:
        """
        Lista los archivos en una carpeta específica.
        """
        dir_path = os.path.join(self.base_folder, folder)
        if not os.path.exists(dir_path):
            return []
        return [f.split(".json")[0] for f in os.listdir(dir_path) if f.endswith(".json")]

    def add_task(self, folder: str, file_name: str, date: str, task: str) -> bool:
        """
        Agrega una nueva tarea a una fecha específica.
        """
        data = self.read_json(folder, file_name) or {}
        if date not in data:
            data[date] = []
        data[date].append({"task": task, "done": False})
        return self.write_json(folder, file_name, data)

    def update_task_status(self, folder: str, file_name: str, date: str, task_index: int, done: bool) -> bool:
        """
        Actualiza el estado de una tarea específica.
        """
        data = self.read_json(folder, file_name)
        if not data or date not in data or task_index >= len(data[date]):
            return False
        data[date][task_index]["done"] = done
        return self.write_json(folder, file_name, data)

    def get_tasks_for_date(self, folder: str, file_name: str, date: str) -> List[Dict[str, Any]]:
        """
        Obtiene todas las tareas de una fecha específica.
        """
        data = self.read_json(folder, file_name)
        return data.get(date, [])

    def move_unfinished_tasks(self, folder: str, file_name: str, current_date: str, next_date: str) -> bool:
        """
        Mueve las tareas no hechas de una fecha actual a la siguiente fecha.
        """
        data = self.read_json(folder, file_name) or {}
        if current_date not in data:
            return False
        unfinished_tasks = [task for task in data[current_date] if not task["done"]]
        if not unfinished_tasks:
            return False
        if next_date not in data:
            data[next_date] = []
        data[next_date].extend(unfinished_tasks)
        data[current_date] = [task for task in data[current_date] if task["done"]]
        return self.write_json(folder, file_name, data)

    def delete_file(self, folder: str, file_name: str) -> bool:
        """
        Elimina un archivo JSON por completo.
        """
        file_path = self._get_file_path(folder, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
def load_projects_data(filename="projects_data.json"):
    """Loads project data from the JSON file."""
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_project_data(project_data, filename="data/projects.json"):
    """Saves project data to the JSON file."""
    with open(filename, "w") as file:
        json.dump(project_data, file, indent=4)