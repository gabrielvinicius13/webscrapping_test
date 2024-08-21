# Projeto de Web Scraping para Leilões Públicos da Conab

Este projeto é um script de web scraping desenvolvido em Python, que automatiza o processo de extração de informações de páginas de leilões públicos disponíveis no site da Conab. O script percorre as páginas do site, extrai informações de interesse, baixa arquivos PDF e os organiza em diretórios locais.

## Funcionalidades

- **Extração de Dados:** Captura textos dos elementos `<h2>` e `<p>` nas páginas de leilões públicos.
- **Download de PDFs:** Baixa arquivos PDF relacionados a cada leilão.
- **Organização dos Dados:** Cria pastas para cada leilão, salvando informações extraídas e PDFs baixados em suas respectivas pastas.
- **Paginação Automática:** Percorre automaticamente todas as páginas de resultados, respeitando um limite configurável pelo usuário.

## Pré-requisitos

- **Python 3.x**
- **Bibliotecas Python:** 
  - `requests`
  - `selenium`
  - `beautifulsoup4`

## Instalação

1. **Clone este repositório:**

   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git
   cd seu-repositorio

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
python -m venv venv
source venv/bin/activate  # Para Linux/Mac
.\venv\Scripts\activate   # Para Windows

## Instale as dependências:
3.  ```bash
    pip install -r requirements.txt

## Configuração do WebDriver
O script utiliza o Selenium WebDriver para interagir com o navegador. É necessário instalar o ChromeDriver:

Baixe o ChromeDriver compatível com a versão do seu Google Chrome em: ChromeDriver.
Descompacte o ChromeDriver e adicione-o ao seu PATH, ou coloque o executável na mesma pasta do script.

## Uso

Para executar o script, ajuste as variáveis conforme necessário e execute:

`python mudando_o_projeto.py`

## Personalização
- Limite de Páginas: O número de páginas a serem processadas pode ser ajustado alterando a variável limite_paginas.
Página Inicial: Para começar a partir de uma página específica, ajuste url_atual para a URL desejada.
Exemplo de Código
O seguinte código ilustra o funcionamento básico do script:

```bash
# Defina o número máximo de páginas que deseja processar
limite_paginas = 3  

# Começa a partir da página 0
pagina_atual = 0  

# URL da página inicial (modifique para começar de outra página)
url_atual = urljoin(url_base, "?start=0")  

while url_atual and pagina_atual < limite_paginas:
    processar_pagina(url_atual)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    url_atual = proxima_pagina(soup, pagina_atual)
    pagina_atual += 1

# Fecha o navegador após o processo
driver.quit()
```

## Estrutura do Projeto
- webscraping.py: Script principal que realiza o web scraping.
- requirements.txt: Lista de dependências do projeto.
- README.md: Documentação do projeto.
## Contribuição
- Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença
Este projeto está licenciado sob a MIT License.
