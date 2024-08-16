from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import re

# Configurar o driver do Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar no modo headless
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")

# Inicializa o WebDriver com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)   
# Acessa o site da Conab
driver.get('https://www.conab.gov.br/comercializacao/leiloes-publicos/compra-publica')

try:
    # Espera até que os elementos estejam presentes no DOM
    wait = WebDriverWait(driver, 10)
    compras = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.tileItem')))
    
    dados = []

    for compra in compras:
        titulo = compra.find_element(By.CSS_SELECTOR, 'div.tileHeader h2').text
        descricao = compra.find_element(By.CSS_SELECTOR,'div.description p').text
        
        # Expressão regular para capturar o ID e a Data
        id_match = re.search(r'\d{3}\s*-\d{4}', titulo)
        data_match = re.search(r'\d{2}/\d{2}/\d{4}', titulo)

        if id_match and data_match:
            id = id_match.group(0)
            data = data_match.group(0)
            
            dados.append({
                "id": id,
                "data-da-compra": data,
                "titulo": titulo,
                "descricao": descricao
            })
        else:
            print(f"ID ou Data não encontrados no título: {titulo}")

    # Salva os dados acumulados em um arquivo JSON
    with open('dados.json', 'w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii=False, indent=4)
        
    print("JSON salvo com sucesso")

except Exception as e:
    print("Erro ao encontrar o elemento:", e)

finally:
    driver.quit()
