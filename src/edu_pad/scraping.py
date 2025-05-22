import os
import sys
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import argparse

def safe_print(text):
    """Maneja impresión segura para consolas que no soportan Unicode"""
    try:
        print(text)
    except UnicodeEncodeError:
        # Reemplaza emojis en caso de error
        cleaned = text.replace('🔍', '[BUSCAR]').replace('📊', '[DATOS]').replace('✅', '[OK]').replace('⚠️', '[ALERTA]')
        print(cleaned)

def get_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.9',
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    try:
        title = soup.find('span',{'class':'vtex-store-components-3-x-productBrand'}).get_text(strip=True)
    except AttributeError:
        title = 'No se encontró el título'

    try:
        price = soup.find('span', {'class': 'vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--product__selling-price-pdp'}).get_text(strip=True)
        if price != 'No se encontró el precio':
            price = f"{price.replace('.', '')}.000"  
    except (AttributeError, ValueError):
        price = 'No se encontró el precio'

    return title, price

def save_to_excel(data, filename="Productos_Panamericana.xlsx"):
    df = pd.DataFrame(data)
    
    df['Precio'] = df['Precio'].apply(
        lambda x: f"{str(x).split('.')[0]}.000" if x != 'No se encontró el precio' else x
    )
    
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        existing_df['Precio'] = existing_df['Precio'].apply(
            lambda x: f"{str(x).split('.')[0]}.000" if x != 'No se encontró el precio' else x
        )
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_excel(filename, index=False)
    return filename

def get_search_results(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.9',
    }

    query_encoded = requests.utils.quote(query)
    url = f"https://www.panamericana.com.co/{query_encoded}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    product_links = []
    for link in soup.find_all('a', {'class': 'vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--global__product-summary h-100 flex flex-column'}, href=True):
        product_links.append("https://www.panamericana.com.co" + link['href'])
    
    return product_links

def main(search_term):
    safe_print(f"🔍 Buscando: {search_term}")
    product_urls = get_search_results(search_term)

    if not product_urls:
        safe_print("⚠️ No se encontraron resultados")
        return

    all_data = []
    safe_print(f"📊 Procesando {len(product_urls[:10])} productos...")
    
    for i, url in enumerate(product_urls[:10]):
        title, price = get_product_info(url)
        safe_print(f"{i+1}. {title[:50]}... - ${price}")

        if title != 'No se encontró el título':
            all_data.append({
                'Fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'Producto': title,
                'Precio': price,
                'URL': url
            })

    if all_data:
        file_name = save_to_excel(all_data)
        safe_print(f"\n✅ Datos guardados en: {file_name}")
    else:
        safe_print("⚠️ No se encontraron productos válidos")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper Automático de Panamericana')
    parser.add_argument('--search', type=str, default='libros', help='Término de búsqueda')
    args = parser.parse_args()
    
    main(args.search)