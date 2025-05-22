import argparse
from scraper.scraping import run_scraper
from scraper.storage.db import DB
from scraper.storage.excel import Excel
import pandas as pd
import sqlite3

def display_results(search_term):
    """Muestra los resultados almacenados en ambos formatos"""
    print("\n" + "="*50)
    print("📊 RESULTADOS OBTENIDOS".center(50))
    print("="*50)
    
    # Mostrar datos de SQLite
    print("\n🔍 DATOS EN BASE DE DATOS SQLite:")
    db_handler = DB()
    try:
        conn = sqlite3.connect(db_handler.db_path)
        df_sqlite = pd.read_sql_query(
            f"SELECT fecha, producto, precio, url FROM Productos_Panamericana WHERE search_term = '{search_term}' ORDER BY fecha DESC",
            conn
        )
        print(df_sqlite.to_string(index=False))
        conn.close()
    except Exception as e:
        print(f"⚠️ Error al leer la base de datos: {e}")
    
    # Mostrar datos de Excel
    print("\n📄 DATOS EN ARCHIVO EXCEL:")
    excel_handler = Excel()
    excel_file = excel_handler.save([], "Productos_Panamericana.xlsx")
    try:
        df_excel = pd.read_excel(excel_file)
        if 'search_term' in df_excel.columns:
            df_excel = df_excel[df_excel['search_term'] == search_term]
        print(df_excel.to_string(index=False))
    except Exception as e:
        print(f"⚠️ Error al leer el archivo Excel: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper Automático de Panamericana')
    parser.add_argument('--search', type=str, default='libros', help='Término de búsqueda')
    args = parser.parse_args()
    
    # Ejecutar el scraper
    run_scraper(args.search)
    
    # Mostrar los resultados obtenidos
    display_results(args.search)