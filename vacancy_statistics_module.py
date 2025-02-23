def predict_rub_salary_hh(vacancy):
    income = vacancy['salary']
    if not income or income['currency'] != 'RUR':
        return None

    return income_calculation(income, 'from', 'to')


def predict_rub_salary_sj(vacancy):
    if not vacancy['payment_from'] and not vacancy['payment_to']:
        return None
    elif vacancy['currency'] != 'rub':
        return None

    return income_calculation(vacancy, 'payment_from', 'payment_to')


def income_calculation(vacancy, income_from, income_to):
    if vacancy[income_from] and vacancy[income_to]:
        return (vacancy[income_from] + vacancy[income_to]) / 2
    elif not vacancy[income_to]:
        return vacancy[income_from] * 1.2
    else:
        return vacancy[income_to] * 0.8


def predict_salary(vacancies, predict_rub_salary):
    vacancy_analytics = {}
    sum_income, count = 0, 0

    for vacancy in vacancies:
        expected_income = predict_rub_salary(vacancy)
        if expected_income:
            sum_income += expected_income
            count += 1
    try:
        vacancy_analytics['num_vacancies'] = count
        vacancy_analytics['average_income'] = int(sum_income / count)
        return vacancy_analytics
    except ZeroDivisionError:
        vacancy_analytics['num_vacancies'] = 0
        vacancy_analytics['average_income'] = 0
        return vacancy_analytics
