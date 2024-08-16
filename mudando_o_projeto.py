import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

# Configuração do WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless (sem janela)
driver = webdriver.Chrome(options=chrome_options)

# URL inicial do site
url_base = "https://www.conab.gov.br/comercializacao/leiloes-publicos/compra-publica"

# Função para limpar texto e remover caracteres inválidos
def limpar_nome(nome):
    nome = re.sub(r'[\\/*?:"<>|]', "", nome)  # Remove caracteres inválidos
    nome = re.sub(r'\s+', ' ', nome)  # Substitui múltiplos espaços por um espaço único
    nome = nome.strip()  # Remove espaços extras no início e no fim
    return nome

# Função para processar uma página
def processar_pagina(url):
    driver.get(url)
    time.sleep(5)  # Espera o carregamento da página

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs_span10 = soup.find_all('div', class_='span10')

    for i, div in enumerate(divs_span10):
        h2_text = div.find('h2').text.strip() if div.find('h2') else f"conteudo_{i+1}"
        pasta_nome = limpar_nome(h2_text)
        pasta_caminho = os.path.join(os.getcwd(), pasta_nome)
        os.makedirs(pasta_caminho, exist_ok=True)

        p_text = div.find('p').text.strip() if div.find('p') else "Sem Descrição"

        with open(os.path.join(pasta_caminho, "informacoes.txt"), "w", encoding='utf-8') as f:
            f.write(f"Título: {h2_text}\n")
            f.write(f"Descrição: {p_text}\n")

        pdf_links = div.find_all('a', href=True)
        
        for link in pdf_links:
            pdf_url = link['href']
            link_text = link.text.strip()

            if pdf_url.startswith('/'):
                pdf_url = urljoin(url, pdf_url)

            response = requests.get(pdf_url)

            if response.status_code == 200:
                pdf_nome = limpar_nome(link_text) + ".pdf"
                pdf_caminho = os.path.join(pasta_caminho, pdf_nome)

                if pdf_nome:
                    with open(pdf_caminho, 'wb') as pdf_file:
                        pdf_file.write(response.content)
                    print(f"Baixado: {pdf_nome} para {pasta_nome}")
                else:
                    print(f"Nome de arquivo inválido, ignorando: {link_text}")
            else:
                print(f"Falha ao baixar {pdf_url}: Status {response.status_code}")

# Função para encontrar o link da próxima página
def proxima_pagina(soup):
    pagination = soup.find('div', class_='pagination row-fluid text-center')
    if pagination:
        ul_tag = pagination.find('ul')
        if ul_tag:
            next_page_link = ul_tag.find('a', class_='pagenav')  # Encontrar o primeiro link com a classe 'pagenav'
            if next_page_link and 'href' in next_page_link.attrs:
                return urljoin(url_base, next_page_link['href'])
    return None

# Limite de páginas a serem processadas
limite_paginas = 2  # Defina o número máximo de páginas que deseja processar
pagina_atual = 0

url_atual = url_base
while url_atual and pagina_atual < limite_paginas:
    processar_pagina(url_atual)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    url_atual = proxima_pagina(soup)
    pagina_atual += 1

# Fecha o navegador
driver.quit()