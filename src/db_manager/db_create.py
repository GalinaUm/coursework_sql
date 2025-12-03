import psycopg2
from psycopg2 import sql

from config import get_db_params


class DatabaseCreator:
    """Класс, создающий таблицы"""

    @staticmethod
    def create_database():
        """Создает базу данных"""
        conn = psycopg2.connect(
            host=get_db_params()["host"],
            dbname=get_db_params()["dbname"],
            user=get_db_params()["user"],
            password=get_db_params()["password"],
            port=get_db_params()["port"]
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(
            "SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s",
            (get_db_params()["dbname"],),
        )
        exists = cur.fetchone()

        if not exists:
            cur.execute(
                sql.SQL("CREATE DATABASE {}").format(
                    sql.Identifier(get_db_params()["dbname"])
                )
            )
            print(f"База данных {get_db_params()['dbname']} создана.")
        else:
            print(f"База данных {get_db_params()['dbname']} уже существует.")
        # cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(get_db_params()["dbname"])))

        cur.close()
        conn.close()
        print(f"База данных {get_db_params()['dbname']} создана")

    @staticmethod
    def create_table():
        """Создает таблицы employers и vacancies"""
        conn = psycopg2.connect(
            host=get_db_params()["host"],
            dbname=get_db_params()["dbname"],
            user=get_db_params()["user"],
            password=get_db_params()["password"],
            port=get_db_params()["port"]
        )
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXIST employers(
                employer_id SERIAL PRIMARY KEY,
                hh_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                url TEXT,
                open_vacancies INT DEFAULT 0
            );
        """
        )

        cur.execute(
            """
            CREATE TABLE IF NOT EXIST vacancies(
                vacancy_id SERIAL PRIMARY KEY,
                hh_id VARCHAR(50) UNIQUE NOT NULL,
                title VARCHAR(255) NOT NULL,
                url TEXT NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                employer_id INTEGER REFERENCES employers(employer_id) ON DELETE CASCADE,
                description TEXT
            );
        """
        )

        conn.commit()
        cur.close()
        conn.close()
        print("Таблицы созданы")
