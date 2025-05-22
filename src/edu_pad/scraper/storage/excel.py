import os
import pandas as pd
from datetime import datetime

class Excel:
    def __init__(self, base_path='src/edu_pad/static/xlsx'):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, data, filename="Productos_Panamericana.xlsx"):
        filepath = os.path.join(self.base_path, filename)
        
        df = pd.DataFrame(data)
        if not df.empty:
            df['Precio'] = df['Precio'].apply(
                lambda x: f"{str(x).split('.')[0]}.000" if x != 'No se encontró el precio' else x
            )
        
        if os.path.exists(filepath):
            existing_df = pd.read_excel(filepath)
            if not df.empty:
                existing_df['Precio'] = existing_df['Precio'].apply(
                    lambda x: f"{str(x).split('.')[0]}.000" if x != 'No se encontró el precio' else x
                )
                df = pd.concat([existing_df, df], ignore_index=True)
            else:
                df = existing_df
        elif df.empty:
            return filepath  # Retorna la ruta incluso si no hay datos nuevos
        
        df.to_excel(filepath, index=False)
        return filepath