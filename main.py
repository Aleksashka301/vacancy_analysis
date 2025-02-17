import requests
from environs import Env
from terminaltables import AsciiTable


def request_response(url, language, location=None, headers=None):
    headers = headers or {}
    params = {}

    if type(location) == int:
        params['per_page'] = 20
        params['text'] = language
        params['area'] = location
    elif type(location) == str:
        params['keywords'] = language
        params['town'] = location

    response = requests.get(url, headers=headers, params=params, timeout=5)
    response.raise_for_status()

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


def predict_salary(vacancies, resource):
    salarys, count = 0, 0
    for vacancy in vacancies:
        if resource == 'hh':
            salary_info = predict_rub_salary_hh(vacancy)
        elif resource == 'sj':
            salary_info = predict_rub_salary_sj(vacancy)

        if salary_info:
            salarys += salary_info
            count += 1

    return count, int(salarys / count)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    sj_secret_key = env.str('SUPERJOB_KEY')

    url_hh = 'https://api.hh.ru/vacancies'
    url_superjob = 'https://api.superjob.ru/2.0/vacancies/'
    headers_sj = {
        'X-Api-App-Id': sj_secret_key,
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
    vacancies_statistics_hh = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]
    vacancies_statistics_sj = [['Язык программирования', 'Вакансий найдено', 'Вакансий обработано', 'Средняя зарплата']]

    for language in programming_languages:
        vacancies_hh = request_response(url_hh, language, 1)
        vacansies_sj = request_response(url_superjob, language, 'Москва', headers_sj)
        average_salary_hh = predict_salary(vacancies_hh['items'], 'hh')
        average_salary_sj = predict_salary(vacansies_sj['objects'], 'sj')

        vacancies_statistics_hh.append([language, vacancies_hh['found'], average_salary_hh[0], average_salary_hh[1]])
        vacancies_statistics_sj.append([language, vacansies_sj['total'], average_salary_sj[0], average_salary_sj[1]])

    table_hh = AsciiTable(vacancies_statistics_hh)
    table_sj = AsciiTable(vacancies_statistics_sj)
    table_hh.title = 'HeadHunter Moscow'
    table_sj.title = 'SuperJob Moscow'

    print(table_hh.table)
    print(table_sj.table)
