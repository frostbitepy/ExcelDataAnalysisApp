import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
from preprocessing import remove_columns, unique_values, filter_values, suma_columna, eliminar_nulls

# Replace 'your_data.xlsx' with the actual path to your Excel file
file_path = 'SINIESTRO21-22.xlsx'
template_file_path = 'SiniestrosAutomovil2022-edited.xlsx'

# Lista de los productos a filtrar
# valid_products = ['AUTOMOVIL- ALTA GAMA','PLAN ACCIONISTAS','REGIONAL','REGIONAL - ITAIPU / CONMEBOL','REGIONAL 0KM','REGIONAL MAX','REGIONAL PLUS','REGIONAL SUPERIOR']
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

# Read the excel file
# df_original = pd.read_excel(file_path)
# df_template = pd.read_excel(template_file_path, valid_products)

def procesar_siniestros(siniestros_df, valid_products, via_importacion):

    # Remove columns that are not needed
    # df = remove_columns(siniestros_df, df_template)
    
    if not valid_products:
        valid_products = products_dict.keys()
    else:
        valid_products = valid_products

    valid_products_code = [products_dict[key] for key in valid_products]
    via_importacion_code = [via_importacion_dict[key] for key in via_importacion]

    # Filtrar por los productos de la lista
    df = filter_values(siniestros_df, 'Producto', valid_products_code)

    # Filtrar por via de importacion seleccionada
    df = filter_values(df, 'Código Via Importación', via_importacion_code)

    # Eliminar filas que no son sinietros
    df = eliminar_nulls(df, 'Fec. Stro.')

    # Sumar los sinietros
    sumatoria_siniestros = suma_columna(df, 'Stro. Auto Cobertura Básica 1')

    # Sumar las filas del dataframe
    sumatoria_filas = len(df)
    
    return {'sumatoria_siniestros': sumatoria_siniestros, 'sumatoria_filas': sumatoria_filas, 'df': df}