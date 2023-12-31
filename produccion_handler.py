import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
from preprocessing import remove_columns, eliminar_filas_por_valor, filter_values, suma_columna
from excel_formulas import generar_devengado
from datetime import datetime, timedelta

# Replace 'your_data.xlsx' with the actual path to your Excel file
# file_path = 'PRODUCCION22-23.xlsx'
# template_file_path = 'ProduccionAutomovil2022-edited.xlsx'

# Read the excel file
# df_original = pd.read_excel(file_path)
# df_template = pd.read_excel(template_file_path)

# Listado de productos a utilizar
# valid_products = ['AUTOMOVIL- ALTA GAMA','FUNCIONARIOS BANCO REGIONAL','PLAN ACCIONISTAS','REGIONAL','REGIONAL - LIDER','REGIONAL - ITAIPU / CONMEBOL','REGIONAL 0KM','REGIONAL MAX','REGIONAL PLUS','REGIONAL SUPERIOR']
# valid_products_code = [1,9,26,34,51,79,91,105,106]
products_dict = {
    'ACOPLADO O CARRETA PLUS': 30,
    'ACOPLADO O CARRETA SUPERIOR 2': 37,
    'ACOPLADO O CARRETA- GS': 17,
    'CAMIONES - SUPERIOR 1': 13,
    'CAMIONES GS': 8,
    'CAMIONES PLUS': 29,
    'CAMIONES SUPERIOR 2': 35,
    'CHILE - REG- GS': 50,
    'FUNCIONARIOS BANCO REGIONAL': 106,
    'GS -REGIONAL 0KM': 91,
    'GS REGIONAL- ALTA GAMA': 51,
    'GS- RC- AUTOMOVILES': 3,
    'GS- REGIONAL - SUDAMERIS': 165,
    'GS-REGIONAL PLUS/MAX': 1,
    'MOTOS ALTA GAMA REG/SUDAMERIS- GS': 52,
    'PERDIDA TOTAL - GS': 5,
    'PERDIDA TOTAL - MOTOCICLETAS': 84,
    'PLAN ACCIONISTAS': 105,
    'REGIONAL - GS': 9,
    'REGIONAL - ITAIPU / CONMEBOL': 85,
    'REGIONAL - MOTOCICLETAS -GS': 20,
    'REGIONAL MAX': 26,
    'REGIONAL SUPERIOR': 34,
    'REGIONAL- FUN.ORSA': 82,
    'REGIONAL- KUROSU / SETAC': 83,
    'RESP. CIVIL AUTOMOVIL - SUPERIOR 2': 33,
    'RESP. CIVIL AUTOMOVILES - PLUS': 27,
    'RESP. CIVIL AUTOMOVILES - SUPERIOR 1': 10,
    'RESP. CIVIL CAMIONES - PLUS': 31,
    'RESP. CIVIL CAMIONES - SUPERIOR 2': 38,
    'RESP. CIVIL CARRETA O ACOP. PLUS': 32,
    'RESP. CIVIL CARRETA O ACOP. SUPERIOR 2': 39,
    'RESP. CIVIL CARRETA O ACOPLADO GS': 24,
    'RESPONSABILIDAD CIVIL & CARTA VERDE': 156,
    'RESPONSABILIDAD CIVIL - MOTOCICLETAS': 21,
    'REGIONAL SUPERIOR': 34
}

via_importacion_dict = {
    'REPRESENTANTE': 1,
    'VIA CHILE': 2,
    'OTROS': 3,
    '': 0
}

def procesar_produccion(produccion_df, inicio_corte, fin_corte, valid_products, via_importacion):
    
    # Remove columns that are not needed
    # df = remove_columns(produccion_df, df_template)

    if not valid_products:
        valid_products = products_dict.keys()
    else:
        valid_products = valid_products

    valid_products_code = [products_dict[key] for key in valid_products]
    via_importacion_code = [via_importacion_dict[key] for key in via_importacion]
    
    # Utilizar solo los productos validos
    df = filter_values(produccion_df, 'Producto', valid_products_code)

    # Filtrar por via de importacion seleccionada
    df = filter_values(df, 'Código Via Importación', via_importacion_code)

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


    
    
