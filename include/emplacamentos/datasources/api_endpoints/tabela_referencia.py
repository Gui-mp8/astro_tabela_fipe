from typing import List, Dict, Any

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from include.emplacamentos.interfaces.endpoints import IEndpoint

class ConsultarTabelaDeReferencia(IEndpoint):
    def create_session(self) -> requests.Session():
        session = None

        if session is None:
            session = requests.Session()
            retries = Retry(total=5,
                            backoff_factor=2,
                            status_forcelist=[500, 502, 503, 504, 520])
            adapter = HTTPAdapter(max_retries=retries)
            session.mount('http://', adapter)
            session.mount('https://', adapter)

        return session

    def get_endpoint_response(self) -> requests.Response:
        response = self.create_session().post(self.endpoint_url)
        if response.status_code == 520:
                print("Server Error (Status Code 520). Skipping this request.")
                return None
        else:
            return response

    def get_endpoint_data(self) -> List[Dict[str, Any]]:
        response = self.get_endpoint_response()

        if response.status_code != 200:
            raise requests.exceptions.RequestException(f"Request failed with status code {response.status_code}")

        try:
            data = response.json()
            return data
        except ValueError:
            raise requests.exceptions.JSONDecodeError("Failed to decode response as JSON", response.text, 0)