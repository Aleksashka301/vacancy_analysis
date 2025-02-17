# Сравниваем вакансии

Скрипт отправляет запросы на два ресурса `Head Hunter` и `SuperJob`. Собирает такие данные о вакансиях как количество
вакансий по выбранному ключевому\ым словам, средний доход, количество обработанных вакансий на странице. Данная
информация выводится в консоль в виде таблицы.

## Установка и запуск скрипта

Для работы скрипта потребуется `python v3.6` и выше.
Скопируйте репозиторий к себе на компьютер:
```python
git clone https://github.com/Aleksashka301/vacancy_analysis
```
В директории со скриптом установите виртуальное окружение
```python
python -m venv myvenv
```
В теминале активируйте виртуальное окружение
```python
myvenv\Scripts\activate
```
Далее, в терминале, установите зависимости
```python
pip install -r requirements.txt
```
В корне скрипта нужно создать файл `.env` с переменными окружения и добавить туда переменные:
- `SUPERJOB_KEY` - ключ необходжимый для отправки запросов на api superjob, его можно получить после регистрации на
сайте `https://api.superjob.ru/`.

После можно запускать скрипт
```python
python main.py
```
Пример вывода:
![Снимок экрана 2025-02-17 180113](https://github.com/user-attachments/assets/2f491324-5d8a-4a94-82b2-2d3c8b8d2b73)


В скрипте есть список с ключевыми словами для поиска, содержимое списка можно изменять для индивидуального поиска
```python
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
```
