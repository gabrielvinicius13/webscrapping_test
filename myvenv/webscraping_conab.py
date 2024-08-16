from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import re
import time

# Configurar o driver do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar no modo headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--print-to-pdf")  # Configuração para salvar como PDF
chrome_options.add_argument("--ignore-certificate-errors")

# # Use o ChromeDriverManager para gerenciar o download do chromedriver
# service = Service(ChromeDriverManager().install())
chrome_options = Options()
# Inicializa o WebDriver com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)   
# Acessa o site da Conab
driver.get('https://www.conab.gov.br/comercializacao/leiloes-publicos/compra-publica')
try:
   # Espera até que o elemento esteja presente no DOM
    wait = WebDriverWait(driver, 10)
    titulo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tileHeader h2')))

    wait = WebDriverWait(driver, 10)
    descricao = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.description p')))
   
    # Extrai o texto

    texto_titulo = titulo.text
    texto_descricao = descricao.text
    
    dados = {
        "titulo":texto_titulo,
        "descricao":texto_descricao
    }
    
    with open('dados.json', 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii = False, indent=1)
    print("Json salvo com sucesso")

    print(texto_titulo)
    print(texto_descricao)
except Exception as e:
    print("Erro ao encontrar o elemento:", e)

finally:
    driver.quit()
