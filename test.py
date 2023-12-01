from produccion_handler import procesar_produccion
import pandas as pd

file_path = 'Producción Automovil 2022.xlsx'

df_original = pd.read_excel(file_path)

# Crear variable inicio corte y fin corte en formato fecha
inicio_corte = '2022-07-01'
fin_corte = '2023-06-30'

# Convert 'inicio_corte' and 'fin_corte' to datetime objects
inicio_corte = pd.to_datetime(inicio_corte)
fin_corte = pd.to_datetime(fin_corte)

print(procesar_produccion(df_original, inicio_corte, fin_corte))

print(df_original.head())

# acceder al df que devuelve el diccionario de la funcion procesar_produccion
df = procesar_produccion(df_original, inicio_corte, fin_corte)['df']

# convertir a excel el df
df.to_excel('Producción_test.xlsx')



