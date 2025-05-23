import csv
import json
import sqlite3

import settings
from work_parser.dto import Vacancy


class ExportEngine:

    def __init__(self, json_mode: bool, csv_mode: bool, db: bool):
        self.json = json_mode
        self.csv = csv_mode
        self.db = db

        if self.db:
            self.__create_db()

    def __create_db(self):
        conn = sqlite3.connect(settings.DB_PATH)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE vacancy (id integer, name text)")
        conn.close()

    def export(self, vacancies: list[Vacancy]) -> None:
        if self.json:
            with open(settings.JSON_PATH, "w") as file:
                json.dump([vacancy.to_dict() for vacancy in vacancies], file, indent=4, ensure_ascii=False)

        if self.csv:
            vacancies_to_csv = [vacancy.to_dict() for vacancy in vacancies]
            columns = vacancies_to_csv[0].keys()

            with open(settings.CSV_PATH, "w") as file:
                writer = csv.DictWriter(file, columns)
                writer.writeheader()
                writer.writerows(vacancies_to_csv)

        if self.db:
            conn = sqlite3.connect(settings.DB_PATH)
            cursor = conn.cursor()

            cursor.executemany("INSERT INTO vacancy VALUES (?,?)", [vacancy.to_list() for vacancy in vacancies])
            conn.commit()
            conn.close()
