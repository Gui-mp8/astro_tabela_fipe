from datetime import datetime
import os
import pwd
import grp

from include.emplacamentos.datasources.scraper import FipeCode
from include.emplacamentos.datasources.api_endpoints.tabela_referencia import ConsultarTabelaDeReferencia
from include.emplacamentos.datasources.api_endpoints.ano_modelo_codigo_fipe import ConsultarAnoModeloPeloCodigoFipe
from include.emplacamentos.datasources.api_endpoints.todos_os_parametros import ConsultarValorComTodosParametros

from airflow.decorators import dag, task
import pandas as pd

@dag(
    dag_id="emplacamentos",
    description="DAG que extrai dados da tabela fipe",
    schedule="0 22 2 * * ",
    start_date=datetime(2024,4,10),
    catchup=False
)
def emplacamentos():

    @task(task_id="fipe_codes_extraction")
    def task_fipe_codes_extraction():
        base_url = 'https://www.tabelafipebrasil.com/fipe/carros'
        headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 OPR/103.0.0.0'}
        fipe = FipeCode()
        fipe.url_base = base_url
        fipe.headers = headers

        return fipe.get_soup_data()

    @task(task_id="tabela_referencia_extraction")
    def task_tabela_referencia_extraction():
        data = ConsultarTabelaDeReferencia()
        data.endpoint_url = "ConsultarTabelaDeReferencia"

        return data.get_endpoint_data()

    @task(task_id="ano_modelo_extraction")
    def task_ano_modelo_extraction(t1, t2):
        endpoint = ConsultarAnoModeloPeloCodigoFipe(
            codigo_tabela_referencia=t2[0]["Codigo"],
            mes_referencia="2024-04-01"
        )
        endpoint.endpoint_url = "ConsultarAnoModeloPeloCodigoFipe"
        endpoint.dataframe = pd.DataFrame(t1)

        return endpoint.validated_data()

    @task(task_id="tabela_fipe_extraction")
    def task_tabela_fipe_extraction(t3):
        endpoint = ConsultarValorComTodosParametros()
        endpoint.endpoint_url = "ConsultarValorComTodosParametros"
        endpoint.dataframe = pd.DataFrame(t3)

        return endpoint.validated_data()

    t1 = task_fipe_codes_extraction()
    t2 = task_tabela_referencia_extraction()
    t3 = task_ano_modelo_extraction(t1, t2)
    t4 = task_tabela_fipe_extraction(t3)

    [t1, t2] >> t3 >> t4

emplacamentos()

