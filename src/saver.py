import json
import os
from abc import ABC, abstractmethod

from src.vacancies import Vacancy


class Saver(ABC):
    """
    абстрактный метод для сохранения и чтения из файла
    """

    @abstractmethod
    def save_to_file(self):
        pass

    @abstractmethod
    def read_from_file(self):
        pass

    @abstractmethod
    def delete_from_file(self):
        pass


class JSONSaver(Saver):
    """
    Класс для сохранения данных о вакансиях в формате JSON в файл.
    """

    def __init__(self, filename, vacancies=None, directory="data"):
        if vacancies is None:
            vacancies = []
        self.__filename = f'{filename}.json'
        self.vacancies = vacancies
        self.directory = directory

    @property
    def filename(self):
        """
        геттер для filename
        """
        return self.__filename

    def save_to_file(self, filename):
        """
        Сохраняет список вакансий в файл JSON.
        """
        if not isinstance(self.vacancies, list):
            raise ValueError("Ожидается, что объект vacancies является списком.")

        full_path = os.path.join(self.directory, filename)  # Путь к файлу

        try:
            vacancies_data = self.convert_to_list()
            if os.path.exists(full_path):
                self.read_from_file()
                readed_data = self.convert_to_list()
                vacancies_data.extend(readed_data)

            with open(full_path, 'w', encoding='UTF-8') as file:
                json.dump(vacancies_data, file, ensure_ascii=False, indent=4)
            print(f"Данные успешно сохранены в {full_path}")
        except AttributeError:
            raise ValueError("Убедитесь, что каждый элемент vacancies имеет метод to_json.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

    def read_from_file(self):
        """
        получает вакансии из файла
        """
        full_path = os.path.join(self.directory, self.filename)  # Путь к файлу

        with open(full_path, 'r') as f:
            self.vacancies = Vacancy.cast_to_object_list(json.loads(f.read()))

    def delete_from_file(self):
        """
        удаляет вакансии из файла
        """
        pass

    def validate_data(self, user_iteraction):
        """
        проверяет что данные есть
        """
        if self.vacancies:
            self.save_to_file(self.filename)
        else:
            print('нет данных для сохранения')
            user_input = input('хотите повторить запрос? y/n\n')

            if user_input[:2] == 'y':
                os.system('clear')
                user_iteraction()
            else:
                print('ну ок')

    def convert_to_list(self):
        """
        возвращает список словарей ст атрибутами объектов Vacancy
        """
        list_vacancies = []
        for vacancy in self.vacancies:
            list_vacancies.append(vacancy.__dict__())
        return list_vacancies
