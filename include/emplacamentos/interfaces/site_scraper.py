from abc import ABC, abstractmethod
from typing import List, Dict

import requests
from bs4 import BeautifulSoup

class ISiteScraper(ABC):
    def __init__(self):
        self._url_base = None
        self._headers = None

    @property
    def url_base(self):
        return self._url_base

    @url_base.setter
    def url_base(self, value: str):
        self._url_base = value

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, value: str):
        self._headers = value

    @abstractmethod
    def get_response(self) -> requests.Response:
        pass

    @abstractmethod
    def get_soup(self, reponse: str, parser: str) -> BeautifulSoup:
        pass

    @abstractmethod
    def get_soup_data(self) -> List[Dict[str, str]]:
        pass
