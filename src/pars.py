import requests
from accessify import private
from src.vacancies import Vacancy
from abc import ABC, abstractmethod


class Parser(ABC):
    """
    Parser - абстрактный класс, который предоставляет базовую структуру для парсеров вакансий.
    """

    @abstractmethod
    def connect_to_api(self, title):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass


class HHClass(Parser):
    """
    HHClass использует API HH.ru для получения списка вакансий, соответствующих заданному запросу.
    """

    def __init__(self):
        self.__URL = 'https://api.hh.ru/'  # Базовый URL для доступа к API HH.ru
        self.vacancies = []

    @property
    def url(self):
        """
        геттер для url
        """
        return self.__URL

    @private
    def connect_to_api(self, title):
        """
        Получает список вакансий с API HH.ru, соответствующих заданному запросу.
        """
        params = {
            'text': title,
            'page': 0,
            'per_page': 100,
            'only_with_salary': True
        }
        response = requests.get(url=f'{self.url}vacancies', params=params)

        # Проверка статуса ответа
        if response.status_code != 200:
            print(f"Ошибка запроса к API: Статус {response.status_code}")
            return

            # Преобразование ответа в JSON и проверка наличия ключа 'items'
        data = response.json()
        if 'items' not in data:
            print("Ответ API не содержит ключа 'items', проверьте структуру ответа:")
            print(data)
            return
            # создает список вакансий, извлекая данные из ответа API
        vacancies_list = response.json()['items']
        self.vacancies = Vacancy.cast_to_object_list(vacancies_list)

    def get_vacancies(self, title):
        """
        получает список инициализированных оюбъектов класса Vacancy
        """
        self.connect_to_api(title)
        return self.vacancies
