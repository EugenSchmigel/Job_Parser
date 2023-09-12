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