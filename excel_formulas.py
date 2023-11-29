from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def rrc_unidad(y_valor, z_valor):
    if pd.notnull(y_valor) and y_valor > pd.Timedelta(0):
        return z_valor / y_valor.days  # Convert timedelta to days
    else:
        return None  # or return a default value


def reserva_de_riesgo_en_curso(y_valor, aa_valor, x_valor):
    return np.where(y_valor > 0, aa_valor * x_valor, np.nan)


def calcular_devengamiento(fecha_desde, fecha_hasta, inicio_corte, fin_corte):
    # Convertir las fechas a objetos datetime si no son cadenas
    if not isinstance(fecha_desde, str):
        fecha_desde = str(fecha_desde)
    if not isinstance(fecha_hasta, str):
        fecha_hasta = str(fecha_hasta)

    # Extraer solo la parte de la fecha (sin la parte del tiempo)
    fecha_desde = datetime.strptime(fecha_desde[:10], "%Y-%m-%d")
    fecha_hasta = datetime.strptime(fecha_hasta[:10], "%Y-%m-%d")
    inicio_corte = datetime.strptime(inicio_corte, "%Y-%m-%d")
    fin_corte = datetime.strptime(fin_corte, "%Y-%m-%d")

    # Verificar las condiciones y calcular el devengado en días
    if fecha_hasta < inicio_corte or fecha_desde > fin_corte:
        return 0
    elif fecha_desde <= inicio_corte and fecha_hasta <= fin_corte:
        return (fecha_hasta - inicio_corte).days
    elif fecha_desde > inicio_corte and fecha_hasta <= fin_corte:
        return (fecha_hasta - fecha_desde).days
    elif fecha_desde > inicio_corte and fecha_hasta > fin_corte:
        return (fin_corte - fecha_desde).days
    elif fecha_desde < inicio_corte and fecha_hasta > fin_corte:
        return (fin_corte - inicio_corte).days



# Crear una funcion que reciba un dataframe, dos columnas y cree una nueva columna al final con la diferencia del valor de las dos columnas,
# la columna nueva debe llamars "Plazo"
def calcular_plazo(dataframe, columna1, columna2):
    dataframe["Plazo"] = dataframe[columna1] - dataframe[columna2]
    return dataframe


# Crear una función que reciba un dataframe, dos columnas, fecha inicio corte, fecha fin corte
# y cree una nueva columna al final llamada "Devengado" con el valor del devengado aplicando la función calcular_devengamiento
def generar_devengado(dataframe, columna1, columna2, fecha_inicio_corte, fecha_fin_corte):
    # Verificar si las columnas existen en el dataframe
    if columna1 not in dataframe.columns or columna2 not in dataframe.columns:
        print(f"Las columnas {columna1} y/o {columna2} no están presentes en el DataFrame.")
        return None

    # Aplicar la función calcular_devengamiento a cada par de valores de las columnas
    devengado_values = np.vectorize(
        lambda x, y: calcular_devengamiento(x, y, fecha_inicio_corte, fecha_fin_corte)
    )(dataframe[columna1], dataframe[columna2])

    # Crear un nuevo DataFrame con la columna "Devengado"
    nuevo_dataframe = pd.concat([dataframe, pd.DataFrame({"Devengado": devengado_values})], axis=1)

    return nuevo_dataframe


# Crear una funcion que reciba un df y dos columnas y cree una nueva columna al final llamada "RRC Unidad" con el valor del RRC Unidad
# aplicando la funcion rrc_unidad
def generar_rrc_unidad(dataframe, columna1, columna2):
    dataframe["RRC Unidad"] = dataframe.apply(lambda row: rrc_unidad(row[columna1], row[columna2]), axis=1)
    return dataframe 


# Crear una funcion que reciba un df y tres columnas, y genere una nueva columna llamad RRC aplicando la funcion reserva_de_riesgo_en_curso
def generar_rrc(dataframe, columna1, columna2, columna3):
    dataframe["RRC"] = dataframe.apply(lambda row: reserva_de_riesgo_en_curso(row[columna1], row[columna2], row[columna3]), axis=1)
    return dataframe