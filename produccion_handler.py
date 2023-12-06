import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
from preprocessing import remove_columns, eliminar_filas_por_valor, filter_values, suma_columna
from excel_formulas import generar_devengado
from datetime import datetime, timedelta

# Replace 'your_data.xlsx' with the actual path to your Excel file
# file_path = 'PRODUCCION22-23.xlsx'
template_file_path = 'ProduccionAutomovil2022-edited.xlsx'

# Read the excel file
# df_original = pd.read_excel(file_path)
df_template = pd.read_excel(template_file_path)

# Listado de productos a utilizar
valid_products = ['AUTOMOVIL- ALTA GAMA','FUNCIONARIOS BANCO REGIONAL','PLAN ACCIONISTAS','REGIONAL','REGIONAL - LIDER','REGIONAL - ITAIPU / CONMEBOL','REGIONAL 0KM','REGIONAL MAX','REGIONAL PLUS','REGIONAL SUPERIOR']
valid_products_code = [1,9,26,34,51,79,91,105,106]

def procesar_produccion(produccion_df, inicio_corte, fin_corte):
    
    # Remove columns that are not needed
    # df = remove_columns(produccion_df, df_template)

    # Utilizar solo los productos validos
    df = filter_values(produccion_df, 'Producto', valid_products_code)

    # Elininar filas de anulaciones
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

    # Sumar la columna RRC
    suma_rrc = suma_columna(df,'RRC')

    # Sumar la columna RRC sin servicio
    suma_rrc_sin_servicio = suma_columna(df,'RRC sin servicio')

    # Contar las filas donde los valores de la columna RRC no sean cero
    cantidad_rrc = len(df[df['RRC'] != 0])

    return {'suma_rrc': suma_rrc, 'suma_rrc_sin_servicio': suma_rrc_sin_servicio, 'cantidad_rrc': cantidad_rrc, 'df': df}


    
    
