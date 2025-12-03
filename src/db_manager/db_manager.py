from typing import Any, Dict, List

import psycopg2

from .config import get_db_params


class DBManager:
    def __init__(self):
        self.params = get_db_params()

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """
        Получает список всех компаний
        и количество вакансий у каждой компании.
        """

        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()

        cur.execute(
            """
            
        """)