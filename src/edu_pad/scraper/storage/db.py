import sqlite3
import os

class DB:
    def __init__(self, db_path='src/edu_pad/static/db/Productos_Panamericana.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Productos_Panamericana (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            producto TEXT NOT NULL,
            precio TEXT NOT NULL,
            url TEXT NOT NULL,
            search_term TEXT NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()

    def save(self, data, search_term):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for item in data:
            cursor.execute('''
            INSERT INTO Productos_Panamericana (fecha, producto, precio, url, search_term)
            VALUES (?, ?, ?, ?, ?)
            ''', (item['Fecha'], item['Producto'], item['Precio'], item['URL'], search_term))
        
        conn.commit()
        conn.close()
        return self.db_path