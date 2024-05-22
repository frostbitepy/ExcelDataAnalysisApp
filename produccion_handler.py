import pandas as pd
import numpy as np
from preprocessing import eliminar_filas_por_valor
from excel_formulas import generar_devengado


# Funcion para procesar el excel de produccion, claculando el RRC y otros valores necesarios 
# teniendo en cuenta la fecha de inicio_corte y fin_corte recibidos como parametros
def procesar_produccion(produccion_df, inicio_corte, fin_corte):
    
    # Asignar produccion_df a df
    df = produccion_df

    # Eliminar filas de anulaciones de la columna 'Nombre Tipo Póliza'
    df = eliminar_filas_por_valor(df, 'Nombre Tipo Póliza', 'Anulacion')    

    # Convert 'Fec. Hasta Art.' and 'Fec. Desde Art.' to datetime objects if not already
    df['Fec. Hasta Art.'] = pd.to_datetime(df['Fec. Hasta Art.'], errors='coerce')
    df['Fec. Desde Art.'] = pd.to_datetime(df['Fec. Desde Art.'], errors='coerce')

    # Create column 'Plazo'
    df['Plazo'] = (df['Fec. Hasta Art.'] - df['Fec. Desde Art.']).dt.days.astype(float)

    # Handle any NaT (Not a Time) values that might result from the conversion
    # df['Plazo'] = df['Plazo'].fillna(0)

    # Convert 'inicio_corte' and 'fin_corte' to datetime objects
    inicio_corte = pd.to_datetime(inicio_corte)
    fin_corte = pd.to_datetime(fin_corte)

    # Apply the function to create the 'Devengado' column
    df['Devengado'] = df.apply(lambda row: generar_devengado(row, inicio_corte, fin_corte), axis=1).copy()

    # Crear columna RRC Unidad
    df.loc[:, 'RRC Unidad'] = np.where(df['Plazo'] > 0, df['Devengado'] / df['Plazo'], 0).copy()
    # df.loc[:, 'RRC Unidad'] = np.where(df['Plazo'] > 0, round(df['Devengado'] / df['Plazo'], 2), 0).copy() # Redondear a dos decimeles

    # Numeric value handler
    df['RRC Unidad'] = pd.to_numeric(df['RRC Unidad'], errors='coerce')
    df['Prima Técnica Art.'] = pd.to_numeric(df['Prima Técnica Art.'], errors='coerce')
    df['Prima Art.'] = pd.to_numeric(df['Prima Art.'], errors='coerce')

    # Manejo de valores nulos
    df['RRC Unidad'].fillna(0, inplace=True)
    df['Prima Técnica Art.'].fillna(0, inplace=True)
    df['Prima Art.'].fillna(0, inplace=True)

    # Create column 'RRC sin servicio'
    # df.loc[:, 'RRC sin servicio'] = np.where((df['Plazo'] > 0) & (df['RRC Unidad'] > 0), df['RRC Unidad'] * df['Prima Técnica Art.'], 0).copy()
    df.loc[:, 'RRC sin servicio'] = np.where((df['Plazo'] > 0) & (df['RRC Unidad'] > 0), round(df['RRC Unidad'] * df['Prima Técnica Art.'], 2), 0).copy() # Redondear a dos decimeles

    # Create column 'RRC'
    # df.loc[:, 'RRC'] = np.where((df['Plazo'] > 0) & (df['RRC Unidad'] > 0), df['RRC Unidad'] * df['Prima Art.'], 0).copy()
    df.loc[:, 'RRC'] = np.where((df['Plazo'] > 0) & (df['RRC Unidad'] > 0), round(df['RRC Unidad'] * df['Prima Art.'], 2), 0).copy() # Redondear a dos decimeles

    # Return te main production dataframe
    return df


def sumar_rrc(produccion_df):
    # Sumar los valores de la columna 'RRC'
    suma_rrc = produccion_df['RRC'].sum()
    return suma_rrc
    

def sumar_rrc_sin_servicio(produccion_df):
    # Sumar los valores de la columna 'RRC sin servicio'
    suma_rrc_sin_servicio = produccion_df['RRC sin servicio'].sum()
    return suma_rrc_sin_servicio


def cantidad_produccion(produccion_df):
    # Sumar las filas del dataframe
    return len(produccion_df)