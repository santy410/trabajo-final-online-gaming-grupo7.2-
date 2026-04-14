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

# ....Empezamos con el dashboard....
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
st.title("Análisis del Compromiso del Usuario según el rango de edad y el Género de Juego🕹️🎮")
st.markdown("En este panel interactivo analizarás el comportamiento y la persistencia de los jugadores en entornos virtuales. A través de esta interfaz, explorarás la relación entre la edad del usuario y la duración de sus sesiones, identificando los géneros de videojuegos y los rangos de edades con mayores niveles de compromiso.")
 
# Panel lateral izquierdo, filtro para la edad 

with st.sidebar:
    st.header("Filtros de busqueda ⚙️")
    
    # Filtro de Edad Rango 15 a 49
    with st.expander("👤 Rango de Edad", expanded=True):
        st.write("Ajusta la edad para actualizar los gráficos")
        rango_edad = st.slider(
            "Selecciona los años:",
            min_value=15,
            max_value=49,
            value=(15, 49)
        )

    # filtro de Género de Juego
    with st.expander("👾 Género de Juego", expanded=False):
        opciones_genero = df['GameGenre'].unique().tolist()
        seleccion_genero = st.multiselect(
            "Selecciona los géneros:",
            options=opciones_genero,
            default=opciones_genero
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👾 **Análisis hecho por:** \n\n Randy Conde y Santiago Hernandez")

  # filtrado de jugadores

edad_minima = rango_edad[0]
edad_maxima = rango_edad[1]

condicion_edad = (df["Age"] >= edad_minima) & (df["Age"] <= edad_maxima)
condicion_genero = df["GameGenre"].isin(seleccion_genero)

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

# ....pestañas....
lista_pestanas = ["📊 Análisis de Medias", "📈 Relaciones", "📍Relacion edad-tiempo de session" ,"📂 Ver Tabla de Datos"]
pestana1, pestana2, pestana3, pestana4 = st.tabs(lista_pestanas)

# definimos paleta de colores 
mis_colores = ["#1f77b4", "#FF5100", "#003366", "#beee62", "#70ae6e"]


#....PRIMERA PESTAÑA....

with pestana1:
    with st.container(border=True):
        st.header("📊 Análisis de Medias: Tiempo de Sesión y Edad según el Engagement")

        # Definimos columnas 
        col_graf_obj2, col_txt_obj2 = st.columns([7, 3])

        with col_graf_obj2:
            with st.container(border=True):
                st.markdown("**Comparativa: Tiempo de sesion promedio (Minutos) vs. Edad (Años)**")
                
                # Agrupamos para obtener medida
                df_agrupado = df_filtrado.groupby('EngagementLevel')[['AvgSessionDurationMinutes', 'Age']].mean().reset_index()
                
                df_agrupado.columns = ['Nivel de Compromiso', 'Tiempo Promedio (min)', 'Edad Media (años)']
                
                df_plot = df_agrupado.melt(
                    id_vars='Nivel de Compromiso', 
                    value_vars=['Tiempo Promedio (min)', 'Edad Media (años)'],
                    var_name='Métrica Analizada', 
                    value_name='Resultado'
                )
                
                # creamos el grafico
                fig_obj2 = px.bar(
                    df_plot,
                    x='Nivel de Compromiso',
                    y='Resultado',
                    color='Métrica Analizada',
                    barmode='group',
                    color_discrete_sequence=["#4587c5", "#8C00FF"],
                    labels={'Resultado': 'Valor de la Media'}
                )
                
                
                st.plotly_chart(fig_obj2, use_container_width=True)

        with col_txt_obj2:
            with st.container(border=True):
                st.markdown("### 📝 Análisis")
                st.write("""
        En este bloque comparamos dos medidas de tendencia central, para entender cómo varían los hábitos según la fidelidad del jugador.
        
        **Observaciones clave:**
        * **Tiempo de Juego (Azul):** Existe una diferencia bastante clara; a mayor compromiso (*High*), el tiempo promedio de sesión aumenta notoriamente. Esto valida que la retención está ligada a la duración de las partidas.
        * **Edad Media (Morado):** Notamos que la edad se mantiene bastante estable en todos los niveles. 
        
        **Conclusión:** El compromiso en este dataset parece estar más influenciado por la disponibilidad de tiempo para jugar que por un factor de edad.
        """)
                
        st.caption("Nota: Los valores representan el promedio aritmético de la muestra.")

#....SEGUNDA PESTAÑA....

with pestana2:
    st.subheader("Composición Relativa del Nivel de Compromiso por Categoría de Juego")
    col_graf3, col_txt3 = st.columns([7, 3])

    with col_graf3:
        with st.container(border=True):
            st.markdown("### 📊 Análisis de Segmentación")
            df_obj3_counts = df_filtrado.groupby(['GameGenre', 'EngagementLevel']).size().reset_index(name='Cantidad')
            
#hacemos el grafico
            fig_obj3 = px.bar(
                df_obj3_counts, x='GameGenre', y='Cantidad', color='EngagementLevel',
                barmode='stack', color_discrete_sequence=mis_colores
            )
            st.plotly_chart(fig_obj3, use_container_width=True)

    with col_txt3:
        with st.container(border=True):
            st.markdown("### 📊 Análisis")
            st.write("""
Al observar la **composición interna** de las barras, se identifica una **distribución notablemente homogénea** del compromiso en todos los géneros.

**Hallazgos estadísticos:**
* No se aprecia un género que domine claramente en lealtad; tanto *Action* como *Strategy* mantienen proporciones similares de usuarios 'High'.
*Esto sugiere que el género del videojuego no es el factor principal que determina el nivel de compromiso del usuario.

                     """)
        
            