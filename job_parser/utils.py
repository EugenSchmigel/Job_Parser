import os

from vacancy import VacancyActions, Vacancy
from api import SuperJobAPI, HeadHunterAPI

sj_secret_key = os.getenv('SJ_API_KEY')

def user_interaction():
    """ Функция для взаимодействия с пользователем """

    #экземпляр класса для работы с API сайтов с вакансиями
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI(sj_secret_key)

    # экземпляр класса для работы с json файлом
    vacancy_actions = VacancyActions('vacancies.json')

    # ввод информации от пользователя
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()

    # скачать вакансии с платформах SJ и HH
    hh_vacancies = hh_api.get_vacancies(search_query)
    superjob_vacancies = superjob_api.get_vacancies(search_query)


    # создание  экземпляров классов и запрошенной вакание от пользователя
    for vac in superjob_vacancies:
        # словарь "vac" ваканцей с JS
        vacancy = Vacancy.vacancy_dictionary(vac, 'sj')
        # добавить вакансии в json файл
        vacancy_actions.add_vacancy(vacancy)

    for vac in hh_vacancies:
        # словарь "vac" ваканцей с HH
        vacancy = Vacancy.vacancy_dictionary(vac, 'hh')
        # добавить вакансии в json файл
        vacancy_actions.add_vacancy(vacancy)


    # print информацию об отсутствии вакансий
    if not vacancy_actions.get_vacancies():
        print("Нет вакансий, соответствующих заданным критериям.")
        return

    # фильтрация по ключевым словам
    filtered_vacancies = filter_vacancies(vacancy_actions.get_vacancies(), filter_words)
    # если нет вакансии тогда print ...
    if not filtered_vacancies:
        print("Нет вакансий, соответсвующих заданным критериям.")
        return

    # сортировка вакансии
    sorted_vacancies = sort_vacancies(filtered_vacancies)
    # получаем список N сортированных вакансий
    top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

    # Вывод N вакансий в консоль
    print_vacancies(top_vacancies)

def filter_vacancies(vacancies, filter_words):
    """фильтрация по ключевым словам"""
    if not filter_words:
        return vacancies
    # список фильтрованих вакансий
    filtered_vacancies = []

    for vac in vacancies:
        vacancy_longtext = f"{vac.title} {vac.description}"
        if any(word.lower() in vacancy_longtext.lower() for word in filter_words):
            filtered_vacancies.append(vac)
    return filtered_vacancies