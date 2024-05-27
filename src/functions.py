from src.pars import HHClass
from src.vacancies import Vacancy
from src.saver import JSONSaver

hh = HHClass()


def get_filtered_vacancies(vacancies, filter_words):
    """
    фильтрация по ключивым словам (город)
    """
    filtered_by_keywords = []
    for vacancy in vacancies:
        if vacancy.area in filter_words:
            filtered_by_keywords.append(vacancy)
    return filtered_by_keywords


def get_vacancies_by_salary(vacancies, salary_range):
    """
    Фильтрация по диапазону зарплат
    """
    filtered_by_salary = []

    for vacancy in vacancies:
        if salary_range[0] < vacancy.salary < salary_range[1]:
            filtered_by_salary.append(vacancy)

    return filtered_by_salary


def get_top_vacancies(sorted_vacancies, top_n):
    """
    возвращает топ N по зарплате
    """
    return sorted_vacancies[:top_n]


def print_vacancies(vacancies):
    """
    выводит топ вакансии на экран
    """
    for vacancy in vacancies:
        print(vacancy)


def user_interaction():
    """
    Функция взаимодействия с пользователем для поиска вакансий и их сохранения
    """
    user_select = int(input('введите:\n1 - для получения данных с HH\n2 - для загрузки из файла\n'))
    if user_select == 1:
        search_query = input("Введите поисковый запрос: например \033[32mводитель\033[0m\n")
        top_n = int(input("Введите количество вакансий для вывода в топ N:\n"))
        filter_words = input(
            "Введите ключевые слова для фильтрации вакансий: \033[32mНазвания городов через пробел\033[0m\n").split()
        try:
            salary_range = list(
                map(int, input("Введите диапазон зарплат: например \033[32m100000-150000\033[0m\n").split('-')))
        except ValueError:
            print('неправильный диапазон')

        vacancies_list = hh.get_vacancies(search_query)

        filtered_vacancies = get_filtered_vacancies(vacancies_list, filter_words)

        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

        sorted_vacancies = sorted(ranged_vacancies, key=lambda x: x.salary, reverse=True)

        top_vacancies = sorted_vacancies[:top_n]

        print_vacancies(top_vacancies)

        filename = input('введите имя файла для сохранения без .json: ')
        json_saver = JSONSaver(filename, top_vacancies)
        json_saver.validate_data(user_interaction)

    elif user_select == 2:
        filename = input('введите имя файла без .json: ')
        json_saver = JSONSaver(filename)
        json_saver.read_from_file()
        print_vacancies(Vacancy.vacancies)

    else:
        print('wrong input!')
