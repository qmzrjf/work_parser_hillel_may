class Vacancy:
    identificator: int
    name: str

    def to_list(self):
        return [int(self.identificator), self.name]

    def to_dict(self):
        return {
            "name": self.name,
            "identificator": self.identificator
        }
