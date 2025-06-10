import streamlit as st
from ydata_profiling import ProfileReport
import pandas as pd
import os
from datetime import datetime
from scraper.scraping import get_search_results, get_product_info
from scraper.storage.excel import save_to_excel

# Configuración de la página
st.set_page_config(page_title="Panamericana Scraper", layout="wide")

# CSS personalizado
st.markdown("""
<style>
.header {
    color: #2E86C1;
    font-size: 28px !important;
}
.price-tag {
    background-color: #F1C40F;
    color: #000;
    padding: 3px 8px;
    border-radius: 12px;
    font-weight: bold;
    display: inline-block;
}
.success-box {
    background-color: #E8F8F5;
    padding: 12px;
    border-radius: 8px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

def show_data_analysis():
    """Muestra el análisis de datos del archivo Excel"""
    excel_path = os.path.join("src", "edu_pad", "static", "xlsx", "Productos_Panamericana.xlsx")
    
    if os.path.exists(excel_path):
        try:
            df = pd.read_excel(excel_path)
            columnas = ["Fecha", "Producto", "Precio", "URL"]
            df_2 = df[columnas]
            
            st.markdown("## 📊 Análisis Completo de Datos")
            profile = ProfileReport(df_2, title="Dashboard Panamericana")
            st_profile_report(profile)
            
        except Exception as e:
            st.error(f"Error al analizar datos: {str(e)}")
    else:
        st.warning("No hay datos históricos para analizar")

def st_profile_report(profile_report):
    """Muestra el reporte de perfilado"""
    from streamlit.components.v1 import html
    html(profile_report.to_html(), height=1000, scrolling=True)

def main():
    # --- INTERFAZ DE BÚSQUEDA ---
    with st.container():
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown("<h1 class='header'>🛍️ Scraper Panamericana</h1>", unsafe_allow_html=True)
            st.markdown("Busca productos y obtén precios automáticamente")

    st.markdown("---")

    with st.form("search_form"):
        search_query = st.text_input("🔍 Ingresa el producto que deseas buscar:", placeholder="Ej: libros, electrónica...")
        search_button = st.form_submit_button("Buscar Productos")

    if search_button and search_query:
        with st.spinner(f'Buscando "{search_query}"...'):
            product_urls = get_search_results(search_query)

            if product_urls:
                all_data = []
                progress_bar = st.progress(0)
                
                for i, url in enumerate(product_urls[:10]):
                    title, price = get_product_info(url)

                    if title != 'No se encontró el título':
                        with st.expander(f"📦 {title}", expanded=False):
                            col1, col2 = st.columns([4,1])
                            with col1:
                                st.markdown(f"**URL:** {url}")
                            with col2:
                                st.markdown(f"**Precio:**<div class='price-tag'>${price}</div>", unsafe_allow_html=True)
                        
                        all_data.append({
                            'Fecha': datetime.now().strftime('%Y-%m-%d %H:%M'),
                            'Producto': title,
                            'Precio': price,
                            'URL': url,
                            'search_term': search_query
                        })
                    progress_bar.progress((i + 1) / len(product_urls[:10]))

                if all_data:
                    st.success(f"✅ Se encontraron {len(all_data)} productos")
                    
                    st.markdown("### 📋 Resumen de Productos")
                    df = pd.DataFrame(all_data)
                    st.dataframe(
                        df.style.format({'Precio': lambda x: f"${x}"}),
                        height=300,
                        use_container_width=True
                    )
                    
                    file_name = save_to_excel(all_data)
                    st.markdown(f"""
                    <div class="success-box">
                        <b>✓ Datos guardados en:</b><br>
                        {file_name}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Mostrar análisis automáticamente después de guardar
                    show_data_analysis()
                else:
                    st.warning("No se encontraron productos con información completa")
            else:
                st.error("No se encontraron resultados para tu búsqueda")
                st.markdown("""
                **Sugerencias:**
                - Busca solo una palabra del producto que quieres
                """)

    st.markdown("---")
    
    # --- SECCIÓN DE ANÁLISIS MANUAL ---
    if st.button("📈 Mostrar Análisis de Datos Históricos"):
        show_data_analysis()

if __name__ == "__main__":
    main()