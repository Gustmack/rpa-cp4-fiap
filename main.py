from consulta_ibge import consultar_municipios_ibge, buscar_municipio_por_nome
from selenium_interactions import abrir_navegador_e_interagir_com_site
from excel_handler import salvar_dados_no_excel
from utils import remover_acentos
from typing import Optional


def executar_busca() -> None:
    """
    Função principal que realiza o fluxo completo de:
    1. Consultar a API do IBGE para obter uma lista de municípios.
    2. Buscar o município informado pelo usuário.
    3. Realizar a busca no site do IBGE para coletar os dados do município.
    4. Salvar os dados no arquivo Excel.
    O processo pode ser repetido conforme a escolha do usuário.
    """
    
    # Consulta à API para obter a lista de municípios
    municipios = consultar_municipios_ibge()
    
    # Loop para permitir múltiplas consultas, se desejado
    while True:
        if municipios:
            # Solicita o nome do município ao usuário
            nome = input("Digite o nome do município: ").strip()
            # Busca o município pelo nome na lista obtida da API
            resultado: Optional[dict] = buscar_municipio_por_nome(nome, municipios)
            
            if resultado:
                # Obtém a sigla da UF (Unidade Federativa) e o nome da cidade formatado
                uf = resultado['municipio']['microrregiao']['mesorregiao']['UF']['sigla']
                cidade = resultado['municipio']['nome'].replace(" ", "-")
                cidade = remover_acentos(cidade)  # Remove acentos e caracteres especiais
                
                # Monta a URL do site do IBGE para a cidade em questão
                url_site = f"https://cidades.ibge.gov.br/brasil/{uf.lower()}/{cidade.lower()}/panorama"
                
                # Usa Selenium para buscar e interagir com o site, coletando os dados do município
                dados_municipio = abrir_navegador_e_interagir_com_site(url_site, nome, uf)
                
                if dados_municipio:
                    # Salva os dados coletados no arquivo Excel
                    salvar_dados_no_excel(dados_municipio)
                    print("Dados salvos no Excel com sucesso.")
                
                # Pergunta ao usuário se ele deseja realizar outra consulta
                opcao = input("Deseja realizar outra consulta? (s/n): ").lower()
                if opcao != 's':
                    print("Saindo da aplicação.")
                    break
            else:
                # Caso o município não seja encontrado, o usuário pode tentar novamente
                print("Município não encontrado.")
                opcao = input("Deseja tentar novamente? (s/n): ").lower()
                if opcao != 's':
                    print("Saindo da aplicação.")
                    break
        else:
            # Caso ocorra um erro na consulta à API e não haja dados de municípios
            print("Erro ao obter dados dos municípios.")
            break


# Execução do código se o script for executado diretamente
if __name__ == "__main__":
    executar_busca()
