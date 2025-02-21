import requests
from environs import Env
from terminaltables import AsciiTable
from pprint import pprint


def request_response(url, params, headers=None):
    headers = headers or {}
    response = requests.get(url, headers=headers, params=params, timeout=5)
    response.raise_for_status()
    pprint(response.json())
    return response.json()


def predict_rub_salary_hh(vacancy):
    income = vacancy['salary']
    if not income or income['currency'] != 'RUR':
        return None
    elif income['from'] and income['to']:
        return (income['from'] + income['to']) / 2
    elif not income['to']:
        return income['from'] * 1.2
    else:
        return income['to'] * 0.8


def predict_rub_salary_sj(vacancy):
    if not vacancy['payment_from'] and not vacancy['payment_to']:
        return None
    elif vacancy['currency'] != 'rub':
        return None
    elif vacancy['payment_from'] and vacancy['payment_to']:
        return (vacancy['payment_from'] + vacancy['payment_to']) / 2
    elif not vacancy['payment_to']:
        return vacancy['payment_from'] * 1.2
    else:
        return vacancy['payment_to'] + 0.8


def predict_salary(vacancies, function):
    sum_income, count = 0, 0
    for vacancy in vacancies:
        expected_income = function(vacancy)
        if expected_income:
            sum_income += expected_income
            count += 1
    try:
        return count, int(sum_income / count)
    except ZeroDivisionError:
        return 0, 0


if __name__ == '__main__':
    env = Env()
    env.read_env()
    sj_secret_key = env.str('SUPERJOB_KEY')
    hh_town = 1
    sj_town = 'Москва'
    num_vacancies = 100

    hh_url = 'https://api.hh.ru/vacancies'
    sj_url = 'https://api.superjob.ru/2.0/vacancies/'
    sj_headers = {
        'X-Api-App-Id': sj_secret_key,
    }

    hh_params = {
        'per_page': num_vacancies,
        'text': None,
        'area': hh_town,
    }
    sj_params = {
        'keywords': None,
        'town': sj_town,
        'count': num_vacancies,
    }

    programming_languages = [
        'JavaScript',
        # 'Java',
        # 'Python',
        # '1С программист',
        # 'PHP',
        # 'C++',
        # 'C#',
        # 'C программист',
    ]
    hh_vacancies_statistics = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    sj_vacancies_statistics = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]

    for language in programming_languages:
        hh_params['text'] = language
        sj_params['keywords'] = language
        hh_vacancies = request_response(hh_url, hh_params)
        sj_vacansies = request_response(sj_url, sj_params, sj_headers)

        hh_num_vacancies = predict_salary(hh_vacancies['items'], predict_rub_salary_hh)[0]
        hh_average_salary = predict_salary(hh_vacancies['items'], predict_rub_salary_hh)[1]
        sj_num_vacancies = predict_salary(sj_vacansies['objects'], predict_rub_salary_sj)[0]
        sj_average_salary = predict_salary(sj_vacansies['objects'], predict_rub_salary_sj)[1]

        hh_vacancies_statistics.append([language, hh_vacancies['found'], hh_num_vacancies, hh_average_salary])
        sj_vacancies_statistics.append([language, sj_vacansies['total'], sj_num_vacancies, sj_average_salary])

    hh_table = AsciiTable(hh_vacancies_statistics)
    sj_table = AsciiTable(sj_vacancies_statistics)
    hh_table.title = 'HeadHunter Moscow'
    sj_table.title = 'SuperJob Moscow'

    print(hh_table.table)
    print(sj_table.table)
