from datetime import datetime

from include.emplacamentos.datasources.scraper import FipeCode

from airflow.decorators import dag, task

@dag(
    dag_id="emplacamentos",
    description="DAG que extrai dados da tabela fipe",
    schedule="* * * * * ",
    start_date=datetime(2024,4,10),
    catchup=False
)
def emplacamentos():

    @task(task_id="tabela_fipe_extraction")
    def task_tabela_fipe_extraction():
        base_url = 'https://www.tabelafipebrasil.com/fipe/carros'
        headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0'}
        fipe = FipeCode()
        fipe.url_base = base_url
        fipe.headers = headers

        return fipe.get_soup_data()

    t1 = task_tabela_fipe_extraction()
    t1

emplacamentos()

