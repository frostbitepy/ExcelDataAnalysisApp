from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def rrc_unidad(plazo, devengado):
    if pd.notnull(plazo) and pd.notnull(devengado) and devengado > pd.Timedelta(0):
        return plazo / devengado.days  # Convert timedelta to days
    else:
        return None  # or return a default value
   
    
def generar_rrc_unidad(row):
    devengado = pd.to_timedelta(row['Devengado'])
    return rrc_unidad(row['Plazo'], devengado)


def reserva_de_riesgo_en_curso(y_valor, aa_valor, x_valor):
    return np.where(y_valor > 0, aa_valor * x_valor, np.nan)


def generar_devengado(row, inicio_corte, fin_corte):
    if row['Fec. Hasta Art.'] < inicio_corte or row['Fec. Desde Art.'] > fin_corte:
        return 0
    elif row['Fec. Desde Art.'] <= inicio_corte and row['Fec. Hasta Art.'] <= fin_corte:
        return (row['Fec. Hasta Art.'] - inicio_corte).days
    elif row['Fec. Desde Art.'] > inicio_corte and row['Fec. Hasta Art.'] <= fin_corte:
        return (row['Fec. Hasta Art.'] - row['Fec. Desde Art.']).days
    elif row['Fec. Desde Art.'] > inicio_corte and row['Fec. Hasta Art.'] > fin_corte:
        return (fin_corte - row['Fec. Desde Art.']).days
    elif row['Fec. Desde Art.'] < inicio_corte and row['Fec. Hasta Art.'] > fin_corte:
        return (fin_corte - inicio_corte).days
    else:
        return 0

"""
def generar_devengado_aux(row, inicio_corte, fin_corte):
    if row['Fec. Hasta Art.'] < inicio_corte or row['Fec. Desde Art.'] > fin_corte:
        return 0
    elif (row['Fec. Desde Art.'] <= inicio_corte and row['Fec. Hasta Art.'] <= fin_corte):
        return max(0, row['Fec. Hasta Art.'] - inicio_corte)
    elif (row['Fec. Desde Art.'] > inicio_corte and row['Fec. Hasta Art.'] <= fin_corte):
        return row['Fec. Hasta Art.'] - row['Fec. Desde Art.']
    elif (row['Fec. Desde Art.'] > inicio_corte and row['Fec. Hasta Art.'] > fin_corte):
        return min(fin_corte - row['Fec. Desde Art.'], fin_corte - inicio_corte)
    elif (row['Fec. Desde Art.'] < inicio_corte and row['Fec. Hasta Art.'] > fin_corte):
        return fin_corte - inicio_corte
    else:
        return 0
"""


# Crear una funcion que reciba un dataframe, dos columnas y cree una nueva columna al final con la diferencia del valor de las dos columnas,
# la columna nueva debe llamars "Plazo"
def calcular_plazo(dataframe, columna1, columna2):
    dataframe["Plazo"] = dataframe[columna1] - dataframe[columna2]
    return dataframe



# Crear una funcion que reciba un df y tres columnas, y genere una nueva columna llamad RRC aplicando la funcion reserva_de_riesgo_en_curso
def generar_rrc(dataframe, columna1, columna2, columna3):
    dataframe["RRC"] = dataframe.apply(lambda row: reserva_de_riesgo_en_curso(row[columna1], row[columna2], row[columna3]), axis=1)
    return dataframe