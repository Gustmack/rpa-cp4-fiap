import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Função para buscar e salvar os dados do site utilizando Selenium
def abrir_navegador_e_interagir_com_site(url: str, nome_municipio: str, nome_uf: str):
    """
    Abre um navegador usando Selenium, navega até uma URL e coleta os dados do município.
    
    :param url: URL do site a ser visitado.
    :param nome_municipio: Nome do município.
    :param nome_uf: Nome da unidade federativa.
    :return: Dicionário com os dados coletados.
    """
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)

        # Esperar até que o conteúdo da página seja carregado
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="dados"]/panorama-resumo/div/table/tr[2]/td[3]/valor-indicador/div/span[1]'))
        )

        # Tratamento de exceção para cada dado caso esteja nulo
        def extrair_dado(xpath):
            try:
                return driver.execute_script("return arguments[0].textContent;", driver.find_element(By.XPATH, xpath))
            except NoSuchElementException:
                return ""

        # Foi verificado que por "Copy element" não seria possíve buscar os valores da página do IBGE pois são todos com os mesmos dados
        # Com isso foi considerado o "Xpath" como opção para buscar os dados para serem armazenados no projeto
        codigo_do_municipio = extrair_dado('//*[@id="dados"]/panorama-resumo/div/div[1]/div[1]/div/p')
        populacao_ultimo_censo = extrair_dado('//*[@id="dados"]/panorama-resumo/div/table/tr[2]/td[3]/valor-indicador/div/span[1]')
        salario_medio_mensal = extrair_dado('//*[@id="dados"]/panorama-resumo/div/table/tr[9]/td[3]/valor-indicador/div/span[1]')
        matriculas_ensino_fundamental = extrair_dado('//*[@id="dados"]/panorama-resumo/div/table/tr[24]/td[3]/valor-indicador/div/span[1]')
        pip_per_capta = extrair_dado('//*[@id="dados"]/panorama-resumo/div/table/tr[37]/td[3]/valor-indicador/div/span[1]')
        mortalidade_infantil = extrair_dado('//*[@id="dados"]/panorama-resumo/div/table/tr[48]/td[3]/valor-indicador/div/span[1]')
        area_urbanizada = extrair_dado('//*[@id="dados"]/panorama-resumo/div/table/tr[55]/td[3]/valor-indicador/div/span[1]')
        area_unidade_territorial = extrair_dado('//*[@id="dados"]/panorama-resumo/div/table/tr[70]/td[3]/valor-indicador/div/span[1]')

        
        # Espera um tempo adicional para garantir que a interação foi concluída
        time.sleep(5)  # Aguarda 5 segundos para ver o resultado antes de fechar o navegador
        # Fecha o Chrome após a execução
        driver.quit()

        # dicionário com os dados do IBGE baixados
        return {
            "nome_municipio": nome_municipio,
            "nome_uf": nome_uf,
            "codigo_do_municipio": codigo_do_municipio,
            "populacao_ultimo_censo": populacao_ultimo_censo,
            "salario_medio_mensal": salario_medio_mensal,
            "matriculas_ensino_fundamental": matriculas_ensino_fundamental,
            "pip_per_capta": pip_per_capta,
            "mortalidade_infantil": mortalidade_infantil,
            "area_urbanizada": area_urbanizada,
            "area_unidade_territorial": area_unidade_territorial
        }

    except Exception as e:
        print(f"Ocorreu um erro ao interagir com o navegador: {e}")
        driver.quit()
        return None
