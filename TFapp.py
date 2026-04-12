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


            


