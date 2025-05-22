import sqlite3
import os
import pandas as pd

class DB:
    def __init__(self, db_path='src/edu_pad/static/db/Productos_Panamericana.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Inicializa la base de datos y crea la tabla si no existe"""
        with self._get_connection() as conn:
            conn.execute('''
            CREATE TABLE IF NOT EXISTS Productos_Panamericana (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                producto TEXT NOT NULL,
                precio TEXT NOT NULL,
                url TEXT NOT NULL,
                search_term TEXT NOT NULL
            )
            ''')

    def _get_connection(self):
        """Retorna una conexión a la base de datos"""
        return sqlite3.connect(self.db_path)

    def save(self, data, search_term):
        """Guarda los datos en la base de datos"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            for item in data:
                cursor.execute('''
                INSERT INTO Productos_Panamericana (fecha, producto, precio, url, search_term)
                VALUES (?, ?, ?, ?, ?)
                ''', (item['Fecha'], item['Producto'], item['Precio'], item['URL'], search_term))
            conn.commit()
        return self.db_path

    def get_results(self, search_term):
        """
        Obtiene los resultados filtrados por término de búsqueda
        :param search_term: Término de búsqueda para filtrar
        :return: DataFrame con los resultados
        """
        with self._get_connection() as conn:
            query = '''
            SELECT fecha, producto, precio, url 
            FROM Productos_Panamericana 
            WHERE search_term = ? 
            ORDER BY fecha DESC
            '''
            return pd.read_sql_query(query, conn, params=(search_term,))