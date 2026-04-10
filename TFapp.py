import streamlit as st 
import pandas as pd
import plotly.express as px

# 1. Configuración de página
st.set_page_config(
    page_title="Dashboard Gaming",
    page_icon="🎮",
    layout="centered"
)

# 2. Caché y carga de datos
@st.cache_data
def cargar_datos():
    # Usamos el archivo 
    df = pd.read_csv("17. Online Gaming (5).csv")
df = cargar_datos()

# 3. Título principal
st.title("Análisis del Compromiso del Usuario según el Perfil Demográfico y el Género de Juego🕹️🎮")
st.markdown("Exploración interactiva")

