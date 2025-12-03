from typing import List

import psycopg2

from config import get_db_params

from ..api.api import HeadHunter


class DataLoader:

    def __init__(self):
        self.api = HeadHunter()

    def load_employers(self, employer_ids: List[str]) -> None:
        """Загружает работодателей"""
        conn = psycopg2.connect(**get_db_params())
        cur = conn.cursor()

        for hh_id in employer_ids:
            try:
                employer = self.api.get_employer(hh_id)
                cur.execute(
                    """
                    INSERT INTO employers (hh_id, name, url, open_vacancies)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        employer["id"],
                        employer["name"],
                        employer.get("alternate_url"),
                        employer.get("open_vacancies", 0),
                    ),
                )
            except Exception as e:
                print(f"Произошла ошибка {e}.")

            conn.commit()
            cur.close()
            conn.close()
            print("Компании загружены.")

    def load_vacancies(self, employer_ids: List[str]):
        """Загружает вакансии"""
        conn = psycopg2.connect(
            host=get_db_params()["host"],
            dbname=get_db_params()["dbname"],
            user=get_db_params()["user"],
            password=get_db_params()["password"],
            port=get_db_params()["port"]
        )
        cur = conn.cursor()

        for hh_id in employer_ids:
            try:
                vacancies = self.api.get_vacancies(hh_id)
                for vac in vacancies:
                    salary = vac.get("salary") or {}
                    cur.execute(
                        """
                        INSERT INTO vacancies (hh_id, title, url, salary_from, salary_to, employer_id, description)
                        VALUES (%s, %s, %s, %s, %s,
                            (SELECT employer_id FROM employers WHERE hh_id = %s),
                            %s)
                        ON CONFLICT (hh_id) DO NOTHING;
                        """,
                        (
                            vac["id"],
                            vac["name"],
                            vac["alternate_url"],
                            salary.get("from"),
                            salary.get("to"),
                            hh_id,
                            (vac.get("snippet") or {}).get("responsibility", "") or "",
                        ),
                    )
            except Exception as e:
                print(f"Ошибка во время загрузки вакансий для {hh_id}: {e}")

        conn.commit()
        cur.close()
        conn.close()
        print("Вакансии загружены.")
