from datetime import datetime
from .utils import safe_print, get_product_info, get_search_results
from .config import HEADERS
from .storage.excel import Excel
from .storage.db import DB

def run_scraper(search_term):
    # Inicializar handlers de almacenamiento
    excel_handler = Excel()
    db_handler = DB()
    
    safe_print(f"🔍 Buscando: {search_term}")
    product_urls = get_search_results(search_term, HEADERS)

    if not product_urls:
        safe_print("⚠️ No se encontraron resultados")
        return

    all_data = process_products(product_urls, search_term)  # Pasar search_term aquí
    
    if all_data:
        # Guardar en ambos formatos
        excel_file = excel_handler.save(all_data)
        safe_print(f"\n✅ Datos guardados en Excel: {excel_file}")
        
        db_file = db_handler.save(all_data, search_term)
        safe_print(f"✅ Datos guardados en SQLite: {db_file}")
    else:
        safe_print("⚠️ No se encontraron productos válidos")

def process_products(product_urls, search_term, max_products=10):
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
                'URL': url,
                'search_term': search_term  # Añadimos el término de búsqueda
            })
    
    return all_data
def process_products(product_urls, search_term, max_products=10):
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
                'URL': url,
                'Busqueda': search_term
            })
    
    return all_data