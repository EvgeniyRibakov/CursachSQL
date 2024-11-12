import psycopg2
from config import config
from typing import List, Tuple


class DBManager:
    def __init__(self):
        params = config()
        self.conn = psycopg2.connect(**params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        query = """
        SELECT c.name, COUNT(v.id) as vacancies_count
        FROM companies c
        LEFT JOIN vacancies v ON c.id = v.company_id
        GROUP BY c.name;
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, str]]:
        query = """
        SELECT c.name, v.title, v.salary, v.url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.id;
        """
        self.cur.execute(query)
        return self.cur.fetchall()

    def get_avg_salary(self) -> float:
        query = "SELECT AVG(salary) FROM vacancies WHERE salary IS NOT NULL;"
        self.cur.execute(query)
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, int, str]]:
        avg_salary = self.get_avg_salary()
        query = "SELECT c.name, v.title, v.salary, v.url FROM vacancies v JOIN companies c ON v.company_id = c.id WHERE v.salary > %s;"
        self.cur.execute(query, (avg_salary,))
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, int, str]]:
        query = "SELECT c.name, v.title, v.salary, v.url FROM vacancies v JOIN companies c ON v.company_id = c.id WHERE v.title ILIKE %s;"
        self.cur.execute(query, (f"%{keyword}%",))
        return self.cur.fetchall()

    def close(self):
        self.cur.close()
        self.conn.close()
