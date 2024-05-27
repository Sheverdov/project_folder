from accessify import private


class Vacancy:
    """
    класс представления вакансии
    """

    title: str  # Название вакансии
    url: str  # URL страницы вакансии
    salary: int  # Зарплата предложенная за работу
    area: str
    schedule: str  # требования по графику
    vacancies = []

    def __init__(self, params):
        self.validate_params(params)
        self.title = params.get('name')
        self.__url = params.get('alternate_url')
        self.area = (params.get('area') or None).get('name')
        self.schedule = params.get('schedule').get('name')
        self.salary = (params.get('salary').get('from')) if params['salary']['from'] else params.get('salary').get('to')

    @private
    def validate_params(self, params):
        """
        проверяет что входные данные имеют тип dict
        """
        if not isinstance(params, dict):
            raise Exception('некорректные данные')

    @classmethod
    def new_vacancy(cls, params):
        """
        возвращает объект класса Vacancy
        """
        return cls(params)

    @classmethod
    def add_vacancy(cls, vacancies):
        """
        добавляет новые вакансии
        """
        for vacancy in vacancies:
            cls.vacancies.append(cls.new_vacancy(vacancy))

    @classmethod
    def convert_to_list(cls):
        """
        преобразует данные в список словарей
        """
        list_vacancies = []
        for vacancy in cls.vacancies:
            list_vacancies.append(vacancy.__dict__())
        return list_vacancies

    @property
    def url(self):
        """
        возвращает url объекта класса Vacancy
        """
        return self.__url

    @classmethod
    def cast_to_object_list(cls, vacancies):
        """
        возвращает список инициализированных объектов класса Vacancy
        """
        cls.vacancies = []
        for vacancy in vacancies:
            cls.vacancies.append(cls.new_vacancy(vacancy))
        return cls.vacancies

    def __str__(self):
        """
        Строковое представление объекта
        """
        return f'title\t\t{self.title}\nurl\t\t{self.url}\nschedule\t{self.schedule}\ncity\t\t{self.area}\nsalary\t\t{self.salary}\n'

    def __repr__(self):
        """
        отладочное строковое представление объекта
        """
        return f'\n{self.title}\t{self.schedule}\t{self.salary}'

    def __gt__(self, other):
        """
        Определение поведения для оператора '>'. Сравнивает вакансии по зарплате
        """
        return self.salary > other.salary

    def __dict__(self):
        """
        сериализатор
        """
        return {
            'name': self.title,
            'alternate_url': self.url,
            'salary': {'from': self.salary},
            'area': {'name': self.area},
            'schedule': {'name': self.schedule}
        }
