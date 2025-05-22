import requests
from bs4 import BeautifulSoup

def safe_print(text):
    """Maneja impresión segura para consolas que no soportan Unicode"""
    try:
        print(text)
    except UnicodeEncodeError:
        cleaned = text.replace('🔍', '[BUSCAR]').replace('📊', '[DATOS]').replace('✅', '[OK]').replace('⚠️', '[ALERTA]')
        print(cleaned)

def get_product_info(url, headers):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    try:
        title = soup.find('span',{'class':'vtex-store-components-3-x-productBrand'}).get_text(strip=True)
    except AttributeError:
        title = 'No se encontró el título'

    try:
        price = soup.find('span', {'class': 'vtex-product-price-1-x-currencyInteger'}).get_text(strip=True)
        price = f"{price.replace('.', '')}.000" if price != 'No se encontró el precio' else price
    except (AttributeError, ValueError):
        price = 'No se encontró el precio'

    return title, price

def get_search_results(query, headers):
    query_encoded = requests.utils.quote(query)
    url = f"https://www.panamericana.com.co/{query_encoded}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    return [
        "https://www.panamericana.com.co" + link['href']
        for link in soup.find_all('a', {'class': 'vtex-product-summary-2-x-clearLink'}, href=True)
    ]