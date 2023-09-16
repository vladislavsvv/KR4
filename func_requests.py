from abc import ABC, abstractmethod

import requests

class Vacancy(ABC):
    """Абстрактный класс для работы с вакансиями"""

    @abstractmethod
    def __init__(self, title, link, salary, employer):
        """Конструктор класса"""
        pass

    @abstractmethod
    def compare_salary(self, other_vacancy):
        """Метод для сравнения вакансий по зарплате"""
        pass

    def is_valid(self):
        """Метод для валидации данных вакансии"""
        return all([self.title, self.link, self.salary, self.employer])


class HHVacancy(Vacancy):
    """Класс для работы с вакансиями на сайте hh.ru"""

    def __init__(self, title, link, salary, employer):
        self.title = title
        self.link = link
        self.salary = salary
        self.employer = employer

    def compare_salary(self, other_vacancy):
        if not self.salary and not other_vacancy.salary:
            return 0
        elif not self.salary:
            return -1
        elif not other_vacancy.salary:
            return 1
        else:
            return self.salary > other_vacancy.salary

class SuperjobVacancy(Vacancy):
    """Класс для работы с вакансиями на сайте superjob.ru"""

    def __init__(self, title, link, salary, employer):
        self.title = title
        self.link = link
        self.salary = salary
        self.employer = employer

    def compare_salary(self, other_vacancy):
        if not self.salary and not other_vacancy.salary:
            return 0
        elif not self.salary:
            return -1
        elif not other_vacancy.salary:
            return 1
        else:
            return self.salary > other_vacancy.salary

class HHVacancyAPI:
    """Класс для работы с API сайта hh.ru"""

    URL = "https://api.hh.ru/vacancies"

    def __init__(self, search_text):
        self.search_text = search_text
        self.total = None

    def get_vacancies(self):
        params = {"text": self.search_text}

        response = requests.get(self.URL, params=params)
        if response.status_code == 200:
            data = response.json()
            self.total = data["found"]
            vacancies = data["items"]
            for v in vacancies:
                salary = None
                if v["salary"]:
                    salary = v["salary"]["from"] if v["salary"]["from"] else v["salary"]["to"]
                hh_vacancy = HHVacancy(v["name"], v["alternate_url"], salary, v['employer']['name'])
                yield hh_vacancy
        else:
            raise Exception("Failed to fetch vacancies from HH API")

class SuperjobVacancyAPI:
    """Класс для работы с API сайта superjob.ru"""

    BASE_URL = "https://api.superjob.ru/2.0/vacancies"

    def __init__(self, search_text):
        self.search_text = search_text
        self.api_key = "v3.r.137806889.01aa2f9635eab9a52783619a13c2c30790e4df13.46bc00e41619d70bd0524ae9e7573e6962dda4ff"

    def get_vacancies(self):
        headers = {"X-Api-App-Id": self.api_key}
        params = {"keyword": self.search_text, "town": "Москва"}

        response = requests.get(self.BASE_URL, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            self.total = data["total"]
            vacancies = data["objects"]
            for v in vacancies:
                if v["currency"] == "rub":
                    superjob_vacancy = SuperjobVacancy(v["profession"], v["link"], v["payment_from"], v['client']['title'])
                    yield superjob_vacancy
        else:
            raise Exception("Failed to fetch vacancies from SuperJob API")



