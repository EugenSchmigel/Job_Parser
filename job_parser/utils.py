import os

from vacancy import VacancyActions, Vacancy
from api import SuperJobAPI, HeadHunterAPI

sj_secret_key = os.getenv('SJ_API_KEY')
