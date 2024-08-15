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

# URL do site
url = "https://www.conab.gov.br/comercializacao/leiloes-publicos/compra-publica"
driver.get(url)
time.sleep(5)  # Espera o carregamento da página

# Usando BeautifulSoup para extrair o HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Encontra todas as divs com a classe "span10"
divs_span10 = soup.find_all('div', class_='span10')

# Função para limpar texto e remover caracteres inválidos
def limpar_nome(nome):
    nome = re.sub(r'[\\/*?:"<>|]', "", nome)  # Remove caracteres inválidos
    nome = re.sub(r'\s+', ' ', nome)  # Substitui múltiplos espaços por um espaço único
    nome = nome.strip()  # Remove espaços extras no início e no fim
    return nome

# Processa cada div "span10"
for i, div in enumerate(divs_span10):
    # Extrai o texto do <h2> para usar como nome da pasta
    h2_text = div.find('h2').text.strip() if div.find('h2') else f"conteudo_{i+1}"
    
    # Remove caracteres inválidos para nomes de pastas
    pasta_nome = limpar_nome(h2_text)
    pasta_caminho = os.path.join(os.getcwd(), pasta_nome)
    os.makedirs(pasta_caminho, exist_ok=True)

    # Extrai os textos dos <h2> e <p> dentro da div
    p_text = div.find('p').text.strip() if div.find('p') else "Sem Descrição"

    # Salva as informações em um arquivo .txt
    with open(os.path.join(pasta_caminho, "informacoes.txt"), "w", encoding='utf-8') as f:
        f.write(f"Título: {h2_text}\n")
        f.write(f"Descrição: {p_text}\n")

    # Encontra todos os links de PDF dentro da div
    pdf_links = div.find_all('a', href=True)
    
    # Baixa os PDFs
    for link in pdf_links:
        pdf_url = link['href']
        link_text = link.text.strip()

        # Se o link começar com '/', ajusta para URL absoluta
        if pdf_url.startswith('/'):
            pdf_url = urljoin(url, pdf_url)
        
        # Faz o download do PDF
        response = requests.get(pdf_url)

        # Verifica o status da resposta
        if response.status_code == 200:
            # Remove caracteres inválidos para nomes de arquivos
            pdf_nome = limpar_nome(link_text) + ".pdf"
            pdf_caminho = os.path.join(pasta_caminho, pdf_nome)

            # Evita criar o arquivo se o nome não for válido
            if pdf_nome:
                with open(pdf_caminho, 'wb') as pdf_file:
                    pdf_file.write(response.content)
                print(f"Baixado: {pdf_nome} para {pasta_nome}")
            else:
                print(f"Nome de arquivo inválido, ignorando: {link_text}")
        else:
            print(f"Falha ao baixar {pdf_url}: Status {response.status_code}")

# Fecha o navegador
driver.quit()
