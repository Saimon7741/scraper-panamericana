import argparse
import sqlite3
import pandas as pd
from scraper.scraping import run_scraper
from scraper.storage.db import DB
from scraper.storage.excel import Excel

def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        cleaned = (text
                  .replace('📊', '[DATOS]')
                  .replace('🔍', '[BUSCAR]')
                  .replace('✅', '[OK]')
                  .replace('⚠️', '[ALERTA]'))
        print(cleaned)

def display_results(search_term):
    safe_print("\n" + "="*50)
    safe_print(" RESULTADOS OBTENIDOS ".center(50, '='))
    safe_print("="*50)
    
    # Mostrar datos de SQLite
    safe_print("\n[DATOS] DATOS EN BASE DE DATOS SQLite:")
    db = DB()
    try:
        conn = sqlite3.connect(db.db_path)
        df_sqlite = pd.read_sql_query(
            f"SELECT fecha, producto, precio, url FROM Productos_Panamericana WHERE search_term = '{search_term}' ORDER BY fecha DESC",
            conn
        )
        safe_print(df_sqlite.to_string(index=False))
        conn.close()
    except Exception as e:
        safe_print(f"[ALERTA] Error al leer la base de datos: {e}")
    
    # Mostrar datos de Excel
    safe_print("\n[DATOS] DATOS EN ARCHIVO EXCEL:")
    excel = Excel()
    try:
        df_excel = excel.filter_by_search_term(search_term)
        safe_print(df_excel.to_string(index=False))
    except Exception as e:
        safe_print(f"[ALERTA] Error al leer el archivo Excel: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper Automático de Panamericana')
    parser.add_argument('--search', type=str, default='libros', help='Término de búsqueda')
    args = parser.parse_args()
    
    # Ejecutar el scraper
    run_scraper(args.search)
    
    # Mostrar los resultados obtenidos
    display_results(args.search)