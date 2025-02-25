def predict_rub_salary_hh(vacancy):
    income = vacancy['salary']
    if not income or income['currency'] != 'RUR':
        return None

    return calculate_income(income, 'from', 'to')


def predict_rub_salary_sj(vacancy):
    if not vacancy['payment_from'] and not vacancy['payment_to']:
        return None
    elif vacancy['currency'] != 'rub':
        return None

    return calculate_income(vacancy, 'payment_from', 'payment_to')


def calculate_income(vacancy, income_from, income_to):
    if vacancy[income_from] and vacancy[income_to]:
        return (vacancy[income_from] + vacancy[income_to]) / 2
    elif not vacancy[income_to]:
        return vacancy[income_from] * 1.2
    else:
        return vacancy[income_to] * 0.8


def predict_salary(vacancies, predict_rub_salary):
    sum_income, count = 0, 0
    for vacancy in vacancies:
        expected_income = predict_rub_salary(vacancy)
        if expected_income:
            sum_income += expected_income
            count += 1
    try:
        return count, int(sum_income / count)
    except ZeroDivisionError:
        return 0, 0
