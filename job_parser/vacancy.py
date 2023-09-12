import json

class Vacancy:
    """Класс вакансии"""
    def __init__(self, title, url, salary, description, salary_currency):

        self.title = title
        self.url = url
        self.salary = salary
        self.description = description
        self.salary_currency = salary_currency

@classmethod
    def vacancy_dictionary(cls, vac_data, job_source):
        """экземпляры вакансий из словарей с сайтов sj.ru и hh.ru """

        # информация с hh.ru
        if job_source == 'hh':
            title = vac_data.get('name')
            url = vac_data.get('alternate_url')
            vac_salary = vac_data.get('salary')

            if vac_salary:
                if vac_salary.get('to') is None:
                    salary = {'min': vac_salary.get('from'), 'max': 0}
                elif vac_salary.get('from') is None:
                    salary = {'min': 0, 'max': vac_salary.get('to')}
                else:
                    salary = {'min': vac_salary.get('from'), 'max': vac_salary.get('to')}
                vac_salary_currency = vac_salary.get('currency')
            else:
                salary = "Отсутствует"
                vac_salary_currency = "Не указано"
            work = vac_data['snippet'].get('requirement')

        # информация с superjob.ru
        elif job_source == 'sj':
            title = vac_data.get('profession')
            url = vac_data.get('link')
            salary = {'min': vac_data.get('payment_from'), 'max': vac_data.get('payment_to')}
            work = vac_data.get('candidat').replace('\n', '/')
            vac_salary_currency = vac_data.get('currency')
        else:
            raise ValueError(f"Invalid job source: {job_source}")

        return cls(title, url, salary, work, vac_salary_currency)


    def __lt__(self, other):
        return self.salary['min'] < other.salary['min']


    def __str__(self):
        return f"""Вакансия: {self.title}, \n Ссылка: {self.url}, \n Зарплата от: {self.salary['min']}  Зарплата до: {self.salary['max']} \n Валюта: {self.salary_currency}, \n Описание: {self.description}"""


class VacancyActions:
    """сохранения информации в файл"""

    def __init__(self, file_name):
        self.vacancies = []
        self.file_name = file_name

    def add_vacancy(self, vacancy):
        """Добавляем вакансии в json файл"""
        self.vacancies.append(vacancy)
        self.add_vac_to_json()

    def get_vacancies_by_salary(self):
        """Сортируем вакансии по з-п"""
        return sorted(self.vacancies, key=lambda vac: (vac.salary['max'] or 0, vac.salary['min'] or 0), reverse=False)
