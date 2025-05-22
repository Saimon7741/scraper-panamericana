from datetime import datetime
from .utils import safe_print, save_to_excel
from .config import HEADERS
from .utils import get_product_info, get_search_results

def run_scraper(search_term):
    safe_print(f"🔍 Buscando: {search_term}")
    product_urls = get_search_results(search_term, HEADERS)

    if not product_urls:
        safe_print("⚠️ No se encontraron resultados")
        return

    all_data = process_products(product_urls)
    
    if all_data:
        file_name = save_to_excel(all_data)
        safe_print(f"\n✅ Datos guardados en: {file_name}")
    else:
        safe_print("⚠️ No se encontraron productos válidos")

def process_products(product_urls, max_products=10):
    all_data = []
    safe_print(f"📊 Procesando {len(product_urls[:max_products])} productos...")
    
    for i, url in enumerate(product_urls[:max_products]):
        title, price = get_product_info(url, HEADERS)
        safe_print(f"{i+1}. {title[:50]}... - ${price}")

        if title != 'No se encontró el título':
            all_data.append({
                'Fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'Producto': title,
                'Precio': price,
                'URL': url
            })
    
    return all_data