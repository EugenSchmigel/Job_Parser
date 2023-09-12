import json

class Vacancy:
    """Класс вакансии"""
    def __init__(self, title, url, salary, description, salary_currency):

        self.title = title
        self.url = url
        self.salary = salary
        self.description = description
        self.salary_currency = salary_currency