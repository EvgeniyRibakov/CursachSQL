from API import HeadHunterAPI
from db_manager import DBManager


def main():
    # Создание таблиц в базе данных
    from creating_table import create_tables
    create_tables()

    # Инициализация API и базы данных
    api_client = HeadHunterAPI()
    db_manager = DBManager()

    # Пример получения данных с API и вставки в базу данных (заполните своими данными)
    companies = [("Company A",), ("Company B",), ("Company C",)]
    vacancies = api_client.get_vacancies("python")  # Пример запроса с ключевым словом

    # Вставка данных в базу данных (пример)
    for company in companies:
        db_manager.cur.execute("INSERT INTO companies (name) VALUES (%s)", company)
    db_manager.conn.commit()

    for vacancy in vacancies:
        company_id = 1  # Пример, замените на реальный company_id
        title = vacancy['name']
        salary = vacancy['salary']['from'] if vacancy['salary'] else None
        url = vacancy['alternate_url']
        db_manager.cur.execute("INSERT INTO vacancies (company_id, title, salary, url) VALUES (%s, %s, %s, %s)",
                               (company_id, title, salary, url))
    db_manager.conn.commit()

    # Вызов методов DBManager для демонстрации
    print("Список всех компаний и количество вакансий у каждой компании:")
    for company in db_manager.get_companies_and_vacancies_count():
        print(company)

    print("\nСписок всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию:")
    for vacancy in db_manager.get_all_vacancies():
        print(vacancy)

    print("\nСредняя зарплата по вакансиям:")
    print(db_manager.get_avg_salary())

    print("\nСписок всех вакансий, у которых зарплата выше средней по всем вакансиям:")
    for vacancy in db_manager.get_vacancies_with_higher_salary():
        print(vacancy)

    print("\nСписок всех вакансий, в названии которых содержатся переданные в метод слова, например 'python':")
    for vacancy in db_manager.get_vacancies_with_keyword('python'):
        print(vacancy)

    db_manager.close()


if __name__ == "__main__":
    main()
