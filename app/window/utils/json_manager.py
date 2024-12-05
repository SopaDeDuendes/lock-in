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

    def _get_file_path(self, file_name: str) -> str:
        """
        Obtiene la ruta completa del archivo JSON.
        """
        return os.path.join(self.base_folder, f"{file_name}.json")

    def read_json(self, file_name: str) -> List[Dict[str, Any]]:
        """
        Lee un archivo JSON y devuelve su contenido.
        """
        file_path = self._get_file_path(file_name)
        if not os.path.exists(file_path):
            return []
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write_json(self, file_name: str, data: List[Dict[str, Any]]) -> bool:
        """
        Escribe una lista en un archivo JSON.
        """
        file_path = self._get_file_path(file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
