from typing import List, Dict

import requests
from bs4 import BeautifulSoup

from include.emplacamentos.interfaces.site_scraper import ISiteScraper

class FipeCode(ISiteScraper):
    def __init__(self) -> None:
        self.parser = "html.parser"

    def get_response(self) -> requests.Response:
        response = requests.get(url=self.url_base, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"HTTP request failed with status code {response.status_code}")
        return response

    def get_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.get_response().content, self.parser)

    def get_soup_data(self) -> List[Dict[str, str]]:
        soup = self.get_soup()
        fipe_data= []

        for a_tag in soup.find_all('a', title=True):
            if a_tag.get('title').startswith("Tabela FIPE código"):
                code = a_tag.text
                car_model = a_tag.find_next('a', title=True).text
                data_dict = {'code': code, 'car_models': car_model}
                fipe_data.append(data_dict)

        return fipe_data