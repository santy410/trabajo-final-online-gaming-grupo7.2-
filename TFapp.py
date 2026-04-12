import pandas as pd
import streamlit as st 
import pandas as pd
import plotly.express as px

#  Carga de datos
nombre_archivo = "17. Online Gaming (5).csv"
df = pd.read_csv("17. Online Gaming (5).csv")

# Definimos variables a utilizar 
variables_necesarias = ['Age', 'AvgSessionDurationMinutes', 'GameGenre', 'EngagementLevel']

# 3 cuantos nulos hay 
print("conteo de datos nulos por cada variable ")
print(df[variables_necesarias].isnull().sum())

# 4 vista rapida de las 4 variables 
print("vista previa de datos")
print(df[variables_necesarias].head())

#tipos de datos

print("tipos de datos")
print(df[variables_necesarias].dtypes)

print("cuales son los datos")

# cuales generos de juego hay
print(f"generos de juego encontrados: {df['GameGenre'].unique()}")

# niveles de engagement
print(f"niveles de compromiso: {df['EngagementLevel'].unique()}")

print("rango de edad")
print(f"La edad va desde los {df['Age'].min()} hasta los {df['Age'].max()} años.")

print("conteo por cada variable")
print("\nDistribución por Género de Juego:")
print(df['GameGenre'].value_counts())

print("\nDistribución por Nivel de Compromiso:")
print(df['EngagementLevel'].value_counts())

# Empezamos con el dashboard

# 1 Configuración de página
st.set_page_config(
    page_title="Dashboard Gaming",
    page_icon="🎮",
    layout="wide"
)

# 2 Carga de datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv("17. Online Gaming (5).csv")
    return df[['Age', 'AvgSessionDurationMinutes', 'GameGenre', 'EngagementLevel']]

df = cargar_datos()

# 3. Título principal
st.title("Análisis del Compromiso del Usuario según el Perfil Demográfico y el Género de Juego🕹️🎮")
st.markdown("En este panel interactivo analizarás el comportamiento y la persistencia de los jugadores en entornos virtuales. A través de esta interfaz, explorarás la relación entre la edad del usuario y la duración de sus sesiones, identificando los géneros de videojuegos y los perfiles demográficos con mayores niveles de compromiso.")
 
# Panel lateral izquierdo, filtro para la edad 

with st.sidebar:
    st.header("Filtros de busqueda ⚙️")
    st.write("Ajusta el rango de edad para poder actualizar los gráficos")
    
    # Filtro de Edad Rango 15 a 49
    rango_edad = st.slider(
        "Rango de Edad:",
        min_value=15,
        max_value=49,
        value=(15, 49)
    )

    # filtro de Género de Juego
    opciones_genero = df['GameGenre'].unique().tolist()
    seleccion_genero = st.multiselect(
        "Géneros de Videojuegos:",
        options=opciones_genero,
        default=opciones_genero
    )

  # filtrado de jugadores

edad_minima = rango_edad[0]
edad_maxima = rango_edad[1]

condicion_edad = (df["Age"] >= edad_minima) & (df["Age"] <= edad_maxima)
condicion_genero = df["GameGenre"].isin(opciones_genero)

filtro_final = condicion_edad & condicion_genero

# aplicamos filtro para dato final 
df_filtrado = df[filtro_final]

st.write(f"Viendo datos de {len(df_filtrado)} jugadores que cumplen los criterios")

# se divide el espacio para las 4 variables 
col1, col2, col3, col4 = st.columns(4)

# calculamos los valores de cada una

#prom edio de sesiones por minuto  
promedio_tiempo = int(df_filtrado['AvgSessionDurationMinutes'].mean())
col1.metric("Sesión Promedio", f"{promedio_tiempo} min")

# promedio de edad 
edad_promedio = int(df_filtrado['Age'].mean())
col2.metric("Edad Media", f"{edad_promedio} años")

# nivel de engagement 
es_alto = df_filtrado['EngagementLevel'] == 'High'
cuenta_alto = len(df_filtrado[es_alto])
col3.metric("Engagement Alto", f"{cuenta_alto} pers.")

# genero de juego mas jugado 
if len(df_filtrado) > 0:
    genero_frecuente = df_filtrado['GameGenre'].mode()[0]
    col4.metric("Género Top", genero_frecuente)
else:
    col4.metric("Género Top", "Sin datos")

st.divider()

# ponemos pestañas para organizar 
lista_pestanas = ["📊 Gráficos Generales", "📈 Relaciones", "📂 Ver Tabla de Datos"]
pestana1, pestana2, pestana3 = st.tabs(lista_pestanas)

