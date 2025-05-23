import argparse
import os
import shutil
from time import sleep

from bs4 import BeautifulSoup

import settings
from work_parser.dto import Vacancy
from work_parser.export import ExportEngine
from work_parser.parser import Parser
from work_parser.request import RequestEngine


def create_data_directory():
    path = os.path.join(settings.PARENT_DIR, "data")

    try:
        shutil.rmtree(path)
    except FileNotFoundError:
        pass

    os.makedirs(path)


def main(json_mode: bool, db_mode: bool, csv_mode: bool):
    create_data_directory()
    page = settings.START_PAGE
    result = []
    requests_engine = RequestEngine()
    parser_engine = Parser()
    export_engine = ExportEngine(json_mode, csv_mode, db_mode)

    while True:
        page_with_cards = requests_engine.get_response(settings.HOST + settings.JOB_PATH, {"page": page})
        cards = parser_engine.find_cards(BeautifulSoup(page_with_cards.text))
        if not cards:
            break

        for card in cards:
            vacancy = Vacancy()
            identificator = parser_engine.get_id(card)
            vacancy.identificator = identificator
            card_page = requests_engine.get_response(settings.HOST + settings.JOB_PATH + identificator)
            name = parser_engine.get_name(BeautifulSoup(card_page.text))
            vacancy.name = name
            result.append(vacancy)

        if result:
            export_engine.export(result)

        result = []
        page += 1
        if page == 3:
            break
        sleep(0.5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parser for work UA")
    parser.add_argument("--json", action="store_true", default=False, help="JSON opportunity")
    parser.add_argument("--db", action="store_true", default=False, help="DB opportunity")
    parser.add_argument("--csv", action="store_true", default=False, help="CSV opportunity")
    args = parser.parse_args()
    main(args.json, args.db, args.csv)
