import pandas as pd

#  Carga de datos
nombre_archivo = "17. Online Gaming (5).csv"
df = pd.read_csv("17. Online Gaming (5).csv")

# Definimos variables a utilizar 
variables_necesarias = ['Age', 'AvgSessionDurationMinutes', 'GameGenre', 'EngagementLevel']

# 3 cuantos nulos hay 
print("conteo de datos nulos por cada variable ")
print(df[variables_necesarias].isnull().sum())

# 4. Una vista rápida para que veas tus 4 columnas
print("vista previa de datos")
print(df[variables_necesarias].head())



