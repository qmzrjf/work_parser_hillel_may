import requests


class RequestEngine:
    def get_response(self, url: str, params: dict | None = None) -> requests.Response:
        response = requests.get(url=url, params=params)
        return response
