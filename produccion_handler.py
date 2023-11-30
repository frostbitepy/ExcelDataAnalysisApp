import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
from preprocessing import remove_columns, eliminar_filas_por_valor, filter_values, suma_columna
from excel_formulas import generar_devengado
from datetime import datetime, timedelta

# Replace 'your_data.xlsx' with the actual path to your Excel file
file_path = 'PRODUCCION22-23.xlsx'
template_file_path = 'ProduccionAutomovil2022-edited.xlsx'

# Read the excel file
# df_original = pd.read_excel(file_path)
df_template = pd.read_excel(template_file_path)

# Listado de productos a utilizar
valid_products = ['AUTOMOVIL- ALTA GAMA','PLAN ACCIONISTAS','REGIONAL','REGIONAL - ITAIPU / CONMEBOL','REGIONAL 0KM','REGIONAL MAX','REGIONAL PLUS','REGIONAL SUPERIOR']


def procesar_produccion(produccion_df, inicio_corte, fin_corte):
    
    # Utilizar solo los productos validos
    df = filter_values(produccion_df, 'Nombre Producto', valid_products)

    # Elininar filas de anulaciones
    df = eliminar_filas_por_valor(produccion_df, 'Nombre Tipo Póliza', 'Anulacion')

    # Check if columns are not in datetime format
    if not pd.api.types.is_datetime64_any_dtype(df['Fec. Hasta Art.']):
        df['Fec. Hasta Art.'] = pd.to_datetime(df['Fec. Hasta Art.'])

    if not pd.api.types.is_datetime64_any_dtype(df['Fec. Desde Art.']):
        df['Fec. Desde Art.'] = pd.to_datetime(df['Fec. Desde Art.'])

    # Crear columna de Plazo
    df['Plazo'] = df['Fec. Hasta Art.'] - df['Fec. Desde Art.']

    # Check if 'inicio_corte' and 'fin_corte' are already datetime objects
    if not isinstance(inicio_corte, datetime):
        inicio_corte = pd.to_datetime(inicio_corte)

    if not isinstance(fin_corte, datetime):
        fin_corte = pd.to_datetime(fin_corte)

    # Apply the function to create the 'Devengado' column
    df['Devengado'] = df.apply(lambda row: generar_devengado(row, inicio_corte, fin_corte), axis=1)

    # Crear columna RRC Unidad
    df['RRC Unidad'] = np.where(df['Plazo'] > pd.Timedelta(0), df['Devengado'] / df['Plazo'].dt.days, 0)

    # Convert 'Plazo' to floats
    df['Plazo'] = df['Plazo'].dt.days.astype(float)

    # Convert 'RRC Unidad' to float, handling empty strings or non-numeric values
    df['RRC Unidad'] = pd.to_numeric(df['RRC Unidad'], errors='coerce').astype(float)

    # Create column 'RRC'
    df['RRC sin servicio'] = np.where((df['Plazo'] > 0) & (df['RRC Unidad'] > 0), df['RRC Unidad'] * df['Prima Técnica Art.'], 0)

    # Create column 'RRC'
    df['RRC'] = np.where((df['Plazo'] > 0) & (df['RRC Unidad'] > 0), df['RRC Unidad'] * df['Prima Art.'], 0)

    # Sumar la columna RRC
    suma_rrc = suma_columna(df,'RRC')

    # Sumar la columna RRC sin servicio
    suma_rrc_sin_servicio = suma_columna(df,'RRC sin servicio')

    # Contar las filas donde los valores de la columna RRC no sean cero
    cantidad_rrc = df[df['RRC'] != 0]

    return {'suma_rrc': suma_rrc, 'suma_rrc_sin_servicio': suma_rrc_sin_servicio, 'cantidad_rrc': cantidad_rrc, 'df': df}


    
    
