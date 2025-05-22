import os
import pandas as pd

class Excel:
    def __init__(self, base_path='src/edu_pad/static/xlsx'):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)
        self.default_filename = "Productos_Panamericana.xlsx"

    def save(self, data, search_term=None, filename=None):
        """Guarda los datos en Excel asegurando el formato de precios"""
        filename = filename or self.default_filename
        filepath = os.path.join(self.base_path, filename)
        
        df = self._prepare_dataframe(data, search_term)
        
        if os.path.exists(filepath):
            existing_df = self.read_data(filename)
            df = pd.concat([existing_df, df], ignore_index=True)
        
        df.to_excel(filepath, index=False)
        return filepath

    def read_data(self, filename=None):
        """Lee el archivo Excel y devuelve un DataFrame con precios formateados"""
        filename = filename or self.default_filename
        filepath = os.path.join(self.base_path, filename)
        
        if os.path.exists(filepath):
            df = pd.read_excel(filepath, dtype={'Precio': str})
            return self._format_prices(df)
        return pd.DataFrame()

    def get_filtered_results(self, search_term, filename=None):
        """Obtiene resultados filtrados por término de búsqueda"""
        df = self.read_data(filename)
        if not df.empty and 'search_term' in df.columns:
            return df[df['search_term'] == search_term]
        return df

    def _prepare_dataframe(self, data, search_term):
        """Prepara el DataFrame con el formato correcto"""
        df = pd.DataFrame(data)
        if not df.empty:
            df = self._format_prices(df)
            if search_term:
                df['search_term'] = search_term
        return df

    def _format_prices(self, df):
        """Aplica el formato XXX.000 a los precios"""
        if 'Precio' in df.columns:
            df['Precio'] = df['Precio'].apply(
                lambda x: f"{str(x).split('.')[0]}.000" if x != 'No se encontró el precio' else x
            )
        return df