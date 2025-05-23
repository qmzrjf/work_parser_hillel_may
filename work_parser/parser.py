from bs4 import BeautifulSoup, Tag


class Parser:

    def find_cards(self, page: BeautifulSoup) -> list:
        class_ = "card card-hover card-visited wordwrap job-link js-job-link-blank js-hot-block"
        first_card = page.find_all(
            "div",
            class_=class_
        )
        cards = page.find_all(
            "div",
            class_=class_ + " mt-sm sm:mt-lg"
        )
        return cards + first_card

    @staticmethod
    def get_id(card: Tag):
        a_tag = card.find("a")
        identificator = a_tag["href"]
        return identificator.strip("/").split("/")[-1]

    @staticmethod
    def get_name(card: BeautifulSoup) -> str:
        name = card.find("h1")
        return name.text
