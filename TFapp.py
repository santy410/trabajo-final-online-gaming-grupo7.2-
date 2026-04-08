# Importación de librerías necesarias
import streamlit as st
import pandas as pd
import plotly.express as px

# 2. Caché y carga de datos
@st.cache_data
def cargar_datos():
    # Usamos el archivo de referencia de Oliver
    df = pd.read_csv("data_house_price.csv")
    # Convertir fecha si es necesario
    df['date'] = pd.to_datetime(df['date'])
    return df

df = cargar_datos()

# 3. Título principal
st.title("🏠 Análisis de Precios de Viviendas")
st.markdown("Exploración interactiva del mercado inmobiliario usando **Streamlit** y **Plotly**.")

# 4. Configuración de la Barra Lateral (Sidebar)
st.sidebar.header("Filtros de Búsqueda")

# Lista de ciudades únicas para el filtro
ciudades_disponibles = df['city'].unique()
ciudades_seleccionadas = st.sidebar.multiselect(
    "Selecciona Ciudades", 
    options=ciudades_disponibles, 
    default=ciudades_disponibles[:3] # Por defecto 3 ciudades
)

# Filtro numérico (Slider) para el precio
precio_min = float(df['price'].min())
precio_max = float(df['price'].max())

rango_precio = st.sidebar.slider(
    "Rango de Precio ($)",
    min_value=precio_min,
    max_value=precio_max,
    value=(0.0, 1000000.0) # Valores por defecto
)

# Aplicar los filtros al DataFrame
df_filtrado = df[
    (df['city'].isin(ciudades_seleccionadas)) & 
    (df['price'] >= rango_precio[0]) & 
    (df['price'] <= rango_precio[1])
]

# 5. Columnas para Métricas (KPIs)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Viviendas", len(df_filtrado))
col2.metric("Precio Promedio", f"${df_filtrado['price'].mean():,.0f}")
col3.metric("Máx Habitaciones", df_filtrado['bedrooms'].max())
col4.metric("Área Promedio (sqft)", f"{df_filtrado['sqft_living'].mean():,.0f}")

st.markdown("---")

# 6. Pestañas para organizar gráficos
tab1, tab2, tab3 = st.tabs(["Distribución de Precios", "Características", "Ubicación"])

with tab1:
    st.subheader("Distribución del Precio de Inmuebles")
    fig_hist = px.histogram(df_filtrado, x="price", nbins=50, color_discrete_sequence=['#0068c9'])
    st.plotly_chart(fig_hist, use_container_width=True)

with tab2:
    st.subheader("Precio según cantidad de Habitaciones y Baños")
    col_a, col_b = st.columns(2)
    with col_a:
        fig_box = px.box(df_filtrado, x="bedrooms", y="price")
        st.plotly_chart(fig_box, use_container_width=True)
    with col_b:
        fig_scatter = px.scatter(df_filtrado, x="sqft_living", y="price", color="bathrooms")
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab3:
    st.subheader("Precio por Ciudad")
    fig_bar = px.bar(df_filtrado.groupby('city')['price'].mean().reset_index(), 
                     x='city', y='price', title="Precio Promedio por Ciudad")
    st.plotly_chart(fig_bar, use_container_width=True)

# 7. Expansor para mostrar el dataset en crudo
with st.expander("Ver los datos originales de las viviendas"):
    st.dataframe(df_filtrado)
