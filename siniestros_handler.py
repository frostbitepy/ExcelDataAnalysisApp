import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl
from preprocessing import remove_columns, unique_values, filter_values, suma_columna, eliminar_nulls

# Replace 'your_data.xlsx' with the actual path to your Excel file
file_path = 'SINIESTRO21-22.xlsx'
template_file_path = 'SiniestrosAutomovil2022-edited.xlsx'

# Lista de los productos a filtrar
valid_products = ['AUTOMOVIL- ALTA GAMA','PLAN ACCIONISTAS','REGIONAL','REGIONAL - ITAIPU / CONMEBOL','REGIONAL 0KM','REGIONAL MAX','REGIONAL PLUS','REGIONAL SUPERIOR']

# Read the excel file
# df_original = pd.read_excel(file_path)
df_template = pd.read_excel(template_file_path)

def procesar_siniestros(siniestros_df):

    # Remove columns that are not needed
    df = remove_columns(siniestros_df, df_template)

    # Filtrar por los productos de la lista
    df = filter_values(df, 'Nombre Producto', valid_products)

    # Eliminar filas que no son sinietros
    df = eliminar_nulls(df, 'Fec. Stro.')

    # Sumar los sinietros
    sumatoria_siniestros = suma_columna(df, 'Stro. Auto Cobertura Básica 1')

    # Sumar las filas del dataframe
    sumatoria_filas = len(df)
    
    return {'sumatoria_siniestros': sumatoria_siniestros, 'sumatoria_filas': sumatoria_filas, 'df': df}