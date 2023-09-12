import requests
from abc import ABC, abstractmethod

class Abstract_Job_API(ABC):
    """Абстрактный класс"""
    def __init__(self, url):
        self.url = url

    @abstractmethod
    def get_vacancies(self, search_request):
        """Абстрактный метод получить вакансий"""
        pass

class HeadHunterAPI(Abstract_Job_API):
    """получения инфо с сайта hh.ru"""
    def __init__(self):
        super().__init__("https://api.hh.ru/vacancies")

    def get_vacancies(self, search_request):
        """Получит вакансии с сайта hh.ru"""
        vac_list = []

        # Получит информацию с 10 страниц по 20 results на странице
        for i in range(10):
            response = requests.get(self.url,
                                    params={'text': search_request, 'per_page': 20, 'page': i, 'only_with_salary': True})
            # Получение вакансий
            vacancies = response.json().get('items', [])

            # добавить вакансии в список "vac_list"
            for vacancy in vacancies:
                vac_list.append(vacancy)

        return vac_list

class SuperJobAPI(Abstract_Job_API):
    """получения информации с сайта superjob.ru"""
    def __init__(self, secret_key):
        super().__init__("https://api.superjob.ru/2.0/vacancies/")
        self.headers = {'X-Api-App-Id': secret_key}

    def get_vacancies(self, search_request):
        """Получает вакансии с сайта superjob.ru"""

        vac_list = []

        # Получит информацию с 10 страниц по 20 results на странице
        for i in range(10):
            response = requests.get(self.url, headers=self.headers, params={'keyword': search_request, 'no_agreement': 1, 'count': 20, 'page': i})

            # Получение вакансий
            vacancies = response.json().get('objects', [])

            # добавить вакансии в список "vac_list"
            for vacancy in vacancies:
                vac_list.append(vacancy)

        return vac_list
