import requests
from typing import List, Dict

# Função para realizar a consulta à API do IBGE
def consultar_municipios_ibge() -> List[Dict]:
    """
    Faz a consulta à API do IBGE para obter a lista de municípios.
    Retorna uma lista de dicionários com os dados dos municípios.
    """
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/distritos"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Converte a resposta em JSON
        else:
            print(f"Erro na requisição. Status code: {response.status_code}")
            return []
    except Exception as e:
        print(f"Ocorreu um erro ao consultar a API: {e}")
        return []

# Função para buscar um município pelo nome no JSON retornado
def buscar_municipio_por_nome(nome_municipio: str, municipios: List[Dict]) -> Dict:
    """
    Busca um município pelo nome dentro da lista de municípios.
    
    :param nome_municipio: O nome do município a ser buscado.
    :param municipios: A lista de dicionários com os dados dos municípios.
    :return: Dicionário com os dados do município ou None se não for encontrado.
    """
    for municipio in municipios:
        if municipio['municipio']['nome'].lower() == nome_municipio.lower():
            return municipio
    return None
