from abc import ABC, abstractmethod
import requests


class APIClient(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str):
        pass


class HeadHunterAPI(APIClient):
    BASE_URL = "https://api.hh.ru/vacancies"

    def connect(self):
        headers = {
            "User-Agent": "api-test-agent"
        }
        response = requests.get(self.BASE_URL, headers=headers)
        if response.status_code != 200:
            raise Exception("Ошибка подключения к API")
        return response

    def get_vacancies(self, keyword: str):
        self.connect()
        params = {
            "text": keyword,
            "per_page": 10
        }
        response = requests.get(self.BASE_URL, params=params)
        data = response.json()
        return data['items']
