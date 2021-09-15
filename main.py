# --*-- coding: utf-8 --*--
"""Задача №2 Сохранение файла на Яндекс.Диск"""
import os
import requests


class YaUploader:
    """Класс для работы с ЯД"""

    def __init__(self, token: str) -> None:
        """Инициализация объекта

        Args:
            token(str): Токен к API ЯД
        """
        self.token = token

    def get_upload_url(self, file_path: str) -> str:
        """Метод получает ссылку для загрузки файла на ЯД

        Args:
            file_path(str): Путь к файлу, который необходимо загрузить на ЯД

        Returns:
            upload_url (str): URL для загрузки файла
        """
        url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        params = {"path": file_path, "overwrite": True}
        headers = {"Authorization": f"OAuth {self.token}"}
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        upload_url = response.json()["href"]
        return upload_url

    def upload(self, file_path: str) -> str:
        """Метод загружает файл на яндекс диск

        Args:
            file_path(str): Путь к файлу, который необходимо загрузить на ЯД

        Returns:
            result(str): Результат операции
        """
        if not os.path.isfile(file_path):
            result = "Файл не существует"
        else:
            if len(file_path.split("/")) > 1:
                self.create_path(file_path[: file_path.rfind("/")])
            response = requests.put(
                self.get_upload_url(file_path), data=open(file_path, "rb")
            )
            response.raise_for_status()
            result = f"Статус ответа {response.status_code}"
        return result

    def create_dir(self, dir: str) -> None:
        """Метод создания папки

        Args:
            dir(str): Наименование папки

        """
        url = "https://cloud-api.yandex.net/v1/disk/resources"
        params = {"path": dir, "overwrite": True}
        headers = {"Authorization": f"OAuth {self.token}"}
        response = requests.put(url, params=params, headers=headers)
        response.raise_for_status()

    def create_path(self, path: str) -> None:
        """Метод создания структуры папок

        Args:
            path(str): Структура папок

        """
        path_dirs = path.split("/")
        total_path = ""
        for dir in path_dirs:
            total_path += dir + "/"
            self.create_dir(total_path)


if __name__ == "__main__":
    path_to_file = input("Введите путь к файлу: ")
    token = input("Введите token для доступа к Яндекс.Диску: ")
    uploader = YaUploader(token)
    result = uploader.upload(path_to_file)
    print(result)
