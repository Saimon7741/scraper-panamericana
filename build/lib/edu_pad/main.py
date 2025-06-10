import argparse
from .scraper.scraping import run_scraper
from .scraper.storage.db import DB
from .scraper.storage.excel import Excel

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        cleaned = text.replace('📊', '[DATOS]').replace('🔍', '[BUSCAR]') \
                     .replace('✅', '[OK]').replace('⚠️', '[ALERTA]')
        print(cleaned)

def display_results(search_term):
    """Muestra los resultados almacenados en ambos formatos"""
    safe_print("\n" + "="*50)
    safe_print(" RESULTADOS OBTENIDOS ".center(50, '='))
    safe_print("="*50)
    
    # Mostrar datos de SQLite
    safe_print("\n[DATOS] DATOS EN BASE DE DATOS SQLite:")
    try:
        db = DB()
        df_sqlite = db.get_results(search_term)
        safe_print(df_sqlite.to_string(index=False))
    except Exception as e:
        safe_print(f"[ALERTA] Error al leer la base de datos: {e}")
    
    # Mostrar datos de Excel
    safe_print("\n[DATOS] DATOS EN ARCHIVO EXCEL:")
    try:
        df_excel = Excel().get_filtered_results(search_term)
        safe_print(df_excel.to_string(index=False))
    except Exception as e:
        safe_print(f"[ALERTA] Error al leer el archivo Excel: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper Automático de Panamericana')
    parser.add_argument('--search', type=str, default='libros', help='Término de búsqueda')
    args = parser.parse_args()
    
    run_scraper(args.search)
    display_results(args.search)