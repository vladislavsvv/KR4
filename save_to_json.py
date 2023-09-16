import os
import json
from abc import ABC, abstractmethod


class FileStorage(ABC):
    """Абстрактный класс для работы с файлом"""

    @abstractmethod
    def create_file(self):
        pass

    @abstractmethod
    def read_file(self):
        pass

    @abstractmethod
    def write_file(self, data):
        pass

    @abstractmethod
    def delete_file(self):
        pass

class JSONFileStorage(FileStorage):
    """Класс для работы с JSON-файлом"""

    def __init__(self, filename):
        self.filename = filename

    def create_file(self):
        if not os.path.exists(self.filename):
            open(self.filename, "w").close()

    def read_file(self):
        with open(self.filename, "r") as f:
            data = json.load(f)
        return data

    def write_file(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def delete_file(self):
        os.remove(self.filename)