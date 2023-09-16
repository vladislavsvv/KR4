from func_requests import HHVacancyAPI, SuperjobVacancyAPI
from save_to_json import JSONFileStorage
from func_filter import get_salary_input, get_sites_input


def run_console_app(min_salary=None, selected_sites=None):
    # запрашиваем поисковый запрос у пользователя
    search_text = input("Введите поисковый запрос: ")

    # запрашиваем минимальную заработную плату
    min_salary = get_salary_input(input("Введите минимальную желаемую зарплату: "))
    print("Доступные сайты для поиска вакансий: 'head_hunter' и 'superjob'.")
    selected_sites = get_sites_input(
        input("Введите сайты, с которых хотите получить вакансии (через запятую): ").split(','))

    # создаем объекты API
    hh_api = HHVacancyAPI(search_text)
    sj_api = SuperjobVacancyAPI(search_text)

    if selected_sites is None or "head_hunter" in selected_sites:
        print("\nПолучение вакансий с HeadHunter...")
        hh_api = HHVacancyAPI(search_text)

    if selected_sites is None or "superjob" in selected_sites:
        print("\nПолучение вакансий с Superjob...")


    # получаем вакансии с каждой платформы
    hh_vacancies = list(hh_api.get_vacancies())
    sj_vacancies = list(sj_api.get_vacancies())

    # объединяем вакансии в один список
    all_vacancies = hh_vacancies + sj_vacancies

    # сортируем вакансии по зарплате
    if min_salary is not None:
        all_vacancies = [v for v in all_vacancies if v.salary is None or v.salary >= min_salary]
    sorted_vacancies = sorted(all_vacancies, key=lambda x: x.salary if x.salary else 0, reverse=True)


    # выводим на экран топ-10 вакансий
    answer = input("Показать, Топ-10 вакансий. Да/Нет").lower().split()
    if answer != "нет" 'no':
        print("Топ-10 вакансий:")
        for i, v in enumerate(sorted_vacancies[:10]):
            print(f"{i + 1}. {v.title}, зарплата: {v.salary}, работодатель: {v.employer}, ссылка: {v.link}")

    # создаем файл для сохранения вакансий
    filename = "vacancies.json"
    storage = JSONFileStorage(filename)
    storage.create_file()

    # сохраняем вакансии в файл
    vacancy_data = [{"title": v.title, "link": v.link, "salary": v.salary, "employer": v.employer} for v in all_vacancies]
    storage.write_file(vacancy_data)

    # читаем данные из файла и выводим на экран
    print("Чтение данных из файла:")
    data_from_file = storage.read_file()
    for v in data_from_file:
        print(f"{v['title']} ({v['salary']}) ({v['employer']}) - {v['link']}")

if __name__ == "__main__":
    run_console_app()





