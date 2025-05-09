import os
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

st.set_page_config(
    page_title="Panamericana Scraper",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stTextInput input {
        border-radius: 20px;
        padding: 10px 15px;
    }
    .stButton button {
        border-radius: 20px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px 24px;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .product-card {
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        background-color: white;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .price-tag {
        font-weight: bold;
        color: #e63946;
    }
    .header {
        color: #2a9d8f;
    }
    .success-box {
        border-left: 5px solid #4CAF50;
        padding: 10px;
        background-color: #0000;
        border-radius: 0 8px 8px 0;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def get_product_info(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.9',
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    try:
        title = soup.find('span',{'class':'vtex-store-components-3-x-productBrand'}).get_text(strip=True)
    except AttributeError:
        title = 'No se encontró el título'

    try:
        price = soup.find('span', {'class': 'vtex-product-price-1-x-currencyInteger vtex-product-price-1-x-currencyInteger--product__selling-price-pdp'}).get_text(strip=True)
        if price != 'No se encontró el precio':
            price = f"{price.replace('.', '')}.000"  
    except (AttributeError, ValueError):
        price = 'No se encontró el precio'

    return title, price

def save_to_excel(data):
    df = pd.DataFrame(data)
    file_name = "Productos_Panamericana.xlsx"
    
    df['Precio'] = df['Precio'].apply(
        lambda x: f"{str(x).split('.')[0]}.000" if x != 'No se encontró el precio' else x
    )
    
    if os.path.exists(file_name):
        existing_df = pd.read_excel(file_name)
        existing_df['Precio'] = existing_df['Precio'].apply(
            lambda x: f"{str(x).split('.')[0]}.000" if x != 'No se encontró el precio' else x
        )
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_excel(file_name, index=False)
    return file_name

def get_search_results(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'es-ES,es;q=0.9',
    }

    url = f"https://www.panamericana.com.co/{query}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    product_links = []
    for link in soup.find_all('a', {'class': 'vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--global__product-summary h-100 flex flex-column'}, href=True):
        product_links.append("https://www.panamericana.com.co" + link['href'])
    
    return product_links

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
                        'URL': url
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
            else:
                st.warning("No se encontraron productos con información completa")
        else:
            st.error("No se encontraron resultados para tu búsqueda")
            st.markdown("""
            **Sugerencias:**
            - Busca solo una palabra del producto que quieres
            """)

st.markdown("---")