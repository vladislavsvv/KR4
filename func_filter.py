


def get_salary_input(min_salary):
    while True:
        try:
            min_salary = int(min_salary)
            if min_salary > 0:
                return min_salary
            else:
                print("Пожалуйста, введите положительное число.")
        except ValueError:
            print("Пожалуйста, введите корректное число.")


def get_sites_input(selected_sites):
    available_sites = ['head_hunter', 'superjob']
    print("Доступные сайты для поиска вакансий: 'head_hunter' и 'superjob'.")
    while True:
        selected_sites = [site.strip() for site in selected_sites]
        if all(site in available_sites for site in selected_sites) and selected_sites:
            return selected_sites
        else:
            print("Не все введенные сайты доступны. Попробуйте еще раз.")
