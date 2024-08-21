import os
import time
import requests
from requests.exceptions import ChunkedEncodingError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import sqlite3
from PyPDF2 import PdfReader

# Configuração do WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executa o Chrome em modo headless (sem janela)
driver = webdriver.Chrome(options=chrome_options)

# URL inicial do site
url_base = "https://www.conab.gov.br/comercializacao/leiloes-publicos/compra-publica"

# Conectar ao banco de dados SQLite (ou criar se não existir)
conn = sqlite3.connect('informacoes_pdf.db')
cursor = conn.cursor()

# Criar uma tabela para armazenar as informações dos PDFs
cursor.execute('''
    CREATE TABLE IF NOT EXISTS pdf_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        descricao TEXT,
        data_compra TEXT,
        hora_compra TEXT,
        pdf_nome TEXT,
        info_extraida TEXT
    )
''')
conn.commit()


# Função para limpar texto e remover caracteres inválidos
def limpar_nome(nome):
    nome = re.sub(r'[\\/*?:"<>|]', "", nome)  # Remove caracteres inválidos
    nome = re.sub(r'\s+', ' ', nome)  # Substitui múltiplos espaços por um espaço único
    nome = nome.strip()  # Remove espaços extras no início e no fim
    return nome


# Função para extrair informações de um PDF
def extrair_informacao_pdf(pdf_caminho):
    with open(pdf_caminho, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        texto = 'TESTEE'
        for page in reader.pages:
            texto += page.extract_text()
        return texto
    
# Função para processar uma página
def processar_pagina(url):
    driver.get(url)
    time.sleep(2)  # Espera o carregamento da página

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    divs_span10 = soup.find_all('div', class_='span10')

    for i, div in enumerate(divs_span10):
        h2_text = div.find('h2').text.strip() if div.find('h2') else f"conteudo_{i+1}"
        pasta_nome = limpar_nome(h2_text)
        pasta_caminho = os.path.join('C:\\Users\\marlon.negreiros\\Documents\\repositorio vinivius\\webscrapping_test\\mypdfs', pasta_nome)
        os.makedirs(pasta_caminho, exist_ok=True)
        
        #extraindo descrição
        p_text = div.find('p').text.strip() if div.find('p') else "Sem Descrição"

        # Procurar a div com a classe 'tileInfo span2' para extrair a data e hora
        tile_info = div.find_next('div', class_='tileInfo span2')
        if tile_info:
            ul_tag = tile_info.find('ul')
            if ul_tag:
                li_tags = ul_tag.find_all('li')
                data = li_tags[0].text.strip() if len(li_tags) > 0 else "Data não encontrada"
                hora = li_tags[1].text.strip() if len(li_tags) > 1 else "Hora não encontrada"
            else:
                data = "Data não encontrada"
                hora = "Hora não encontrada"
        else:
            data = "Data não encontrada"
            hora = "Hora não encontrada"

        
         # Gravar as informações no arquivo de texto
        with open(os.path.join(pasta_caminho, "informacoes.txt"), "w", encoding='utf-8') as f:
            f.write(f"Título: {h2_text}\n")
            f.write(f"Descrição: {p_text}\n")
            f.write(f"Data da compra: {data}\n")
            f.write(f"Hora da compra: {hora}\n")

        pdf_links = div.find_all('a', href=True)
        
        for link in pdf_links:
            pdf_url = link['href']
            link_text = link.text.strip()

            if pdf_url.startswith('/'):
                pdf_url = urljoin(url, pdf_url)

            try:
                response = requests.get(pdf_url, timeout=30)  # Define um timeout para evitar bloqueios
                response.raise_for_status()

                if response.status_code == 200:
                    pdf_nome = limpar_nome(link_text) + ".pdf"
                    pdf_caminho = os.path.join(pasta_caminho, pdf_nome)

                    if pdf_nome:
                        with open(pdf_caminho, 'wb') as pdf_file:
                            pdf_file.write(response.content)
                        print(f"Baixado: {pdf_nome} para {pasta_nome}")

                         # Extrair informações do PDF
                        info_extraida = extrair_informacao_pdf(pdf_caminho)

                        # Salvar informações no banco de dados
                        cursor.execute('''
                            INSERT INTO pdf_info (titulo, descricao, data_compra, hora_compra, pdf_nome, info_extraida)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (h2_text, p_text, data, hora, pdf_nome, info_extraida))
                        conn.commit()  # Salva as alterações no banco de dados

                    else:
                        print(f"Nome de arquivo inválido, ignorando: {link_text}")
                else:
                    print(f"Falha ao baixar {pdf_url}: Status {response.status_code}")
            
            except (requests.exceptions.RequestException, ChunkedEncodingError) as e:
                print(f"Erro ao baixar {pdf_url}: {e}")

# Função para encontrar o link da próxima página
def proxima_pagina(soup, pagina_atual):
    pagination = soup.find('div', class_='pagination row-fluid text-center')
    if pagination:
        ul_tag = pagination.find('ul')
        if ul_tag:
            # Procurar o link com a classe 'pagenav' e o número da próxima página
            next_page_link = ul_tag.find('a', class_='pagenav', string=str(pagina_atual + 1))
            if next_page_link and 'href' in next_page_link.attrs:
                return urljoin(url_base, next_page_link['href'])
            else:
                # Se não houver um link com o número exato da próxima página, tentar o próximo na lista
                links = ul_tag.find_all('a', class_='pagenav')
                for link in links:
                    href = link['href']
                    page_number_match = re.search(r'start=(\d+)', href)
                    if page_number_match:
                        page_number = int(page_number_match.group(1))
                        if page_number > pagina_atual * 10:  # Assumindo paginação de 10 itens por página
                            return urljoin(url_base, href)
    return None

# Limite de páginas a serem processadas
limite_paginas = 1  # Defina o número máximo de páginas que deseja processar
pagina_atual = 1 # Começa a partir da página

# URL da página 10
url_atual = urljoin(url_base, "?start=0")  # Caso queira pegar a partir de uma pagina especifica

while url_atual and pagina_atual < limite_paginas + 1:  # possivel ajustar o limite para página que desejar
    processar_pagina(url_atual)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    url_atual = proxima_pagina(soup, pagina_atual)
    pagina_atual += 1

# Fecha o navegador
driver.quit()
conn.close()