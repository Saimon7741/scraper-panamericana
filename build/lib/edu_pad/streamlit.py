import streamlit as st
from ydata_profiling import ProfileReport
import pandas as pd
import os



def main():


    

    df = pd.read_xlsx("src/edu_pad/static/xlsx/Productos_Panamericana.xlsx")
    columnas = ["abrir","max","min","cerrar","cierre_ajustado","volumen","indicador"]
    df_2 = df[columnas]
    profile = ProfileReport(df_2, title="Dashboard Indicador Dolar")
    st.title("Análisis de Datos")