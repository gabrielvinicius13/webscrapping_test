# import requests as rq
# import pymupdf as pymu
# from bs4 import BeautifulSoup
# import re

# url_pdf = 'http://alerjln1.alerj.rj.gov.br/scpro1923.nsf/18c1dd68f96be3e7832566ec0018d833/6396cb98d31b5cac0325891f0062bb34?OpenDocument'

# response = rq.get(url_pdf)

# with open('documento3.pdf', 'wb') as file:
#     file.write(response.content)


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

# Configurações para salvar PDF automaticamente
chrome_options = Options()
chrome_options.add_argument("--kiosk-printing")  # Modo de impressão automática
prefs = {
    "printing.print_preview_sticky_settings.appState": '{"recentDestinations":[{"id":"Save as PDF","origin":"local"}],"selectedDestinationId":"Save as PDF","version":2}',
    "savefile.default_directory": os.getcwd()  # Diretório padrão para salvar o PDF
}
chrome_options.add_experimental_option("prefs", prefs)

# Inicializa o WebDriver com as opções configuradas
driver = webdriver.Chrome(options=chrome_options)

# Lista de URLs para serem processadas
urls = [
    'http://www3.alerj.rj.gov.br/lotus_notes/default.asp?id=144&url=L3NjcHJvMTkyMy5uc2YvMThjMWRkNjhmOTZiZTNlNzgzMjU2NmVjMDAxOGQ4MzMvMWNkOGFlMmQwODA2ODk4OTAzMjU4OTFmMDA2M2YwODA/T3BlbkRvY3VtZW50#',
    'http://www3.alerj.rj.gov.br/lotus_notes/default.asp?id=144&url=L3NjcHJvMTkyMy5uc2YvMThjMWRkNjhmOTZiZTNlNzgzMjU2NmVjMDAxOGQ4MzMvOGMwNjYzZTU3ZjkzNTBmOTAzMjU4OGZjMDA1NjkzMGQ/T3BlbkRvY3VtZW50'
    # Adicione mais URLs conforme necessário
]

try:
    # Abre a página desejada
    for url in urls:

        driver.get(url)
        
        # Dá um tempo para a página carregar (ajuste conforme necessário)
        time.sleep(5)

        # Dispara o comando de impressão
        driver.execute_script("window.print();")

        # Tempo para o PDF ser salvo
        time.sleep(5)

finally:
    driver.quit()

# O PDF será salvo automaticamente no diretório atual
