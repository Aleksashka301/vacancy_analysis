from environs import Env
from terminaltables import AsciiTable
from requests_module import request_response
from vacancy_statistics_module import predict_salary, predict_rub_salary_hh, predict_rub_salary_sj


def get_table(vacansies: list, title: str):
    vacancies_statistics = ['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']
    vacansies.insert(0, vacancies_statistics)
    table = AsciiTable(vacansies)
    table.title = title

    return table.table


if __name__ == '__main__':
    env = Env()
    env.read_env()
    sj_secret_key = env.str('SUPERJOB_KEY')
    sj_town = 'Москва'
    hh_town = 1

    hh_url = 'https://api.hh.ru/vacancies'
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    sj_headers = {
        'X-Api-App-Id': sj_secret_key,
    }

    hh_params = {
        'per_page': 10,
        'text': None,
        'area': hh_town,
        'page': 0,
    }
    sj_params = {
        'keywords': None,
        'town': sj_town,
        'page': 0,
        'count': 40,
    }

    programming_languages = [
        'JavaScript',
        'Java',
        'Python',
        '1С программист',
        'PHP',
        'C++',
        'C#',
        'C программист',
    ]
    hh_vacancies_statistics, sj_vacancies_statistics = [], []

    for language in programming_languages:
        hh_params['text'] = language
        hh_all_vacansies = []
        hh_pages = 1
        sj_params['page'] = 0
        sj_params['keywords'] = language
        sj_all_vacansies = []

        while hh_params['page'] < hh_pages:
            hh_vacancies = request_response(hh_url, hh_params)
            hh_all_vacansies.extend(hh_vacancies['items'])
            hh_params['page'] += 1
            hh_pages = hh_vacancies['pages']

        while True:
            sj_vacansies = request_response(sj_url, sj_params, sj_headers)
            sj_all_vacansies.extend(sj_vacansies['objects'])
            sj_params['page'] += 1

            if not sj_vacansies['more']:
                break

        hh_num_vacancies, hh_average_income = predict_salary(hh_all_vacansies, predict_rub_salary_hh)
        hh_vacancies_statistics.append([language, hh_vacancies['found'], hh_num_vacancies, hh_average_income])

        sj_num_vacancies, sj_average_income = predict_salary(sj_all_vacansies, predict_rub_salary_sj)
        sj_vacancies_statistics.append([language, sj_vacansies['total'], sj_num_vacancies, sj_average_income])

    hh_table = get_table(hh_vacancies_statistics, 'HeadHunter Moscow')
    sj_table = get_table(sj_vacancies_statistics, 'SuperJob Moscow')

    print(hh_table)
    print(sj_table)
