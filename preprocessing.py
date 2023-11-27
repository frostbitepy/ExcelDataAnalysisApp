import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl


# Remove columns that are not needed function
# Remove the diferent columns from the df that are not in the template
def remove_columns(df, template):
    for column in df.columns:
        if column not in template.columns:
            df.drop(column, axis=1, inplace=True)
    return df

def remove_columns_with_nulls(df):
    # Drop columns with only null values
    df_cleaned = df.dropna(axis=1, how='all')
    return df_cleaned

def remove_columns_with_zeros(df):
    # Drop columns with only 0 values
    df_cleaned = df.loc[:, (df != 0).any(axis=0)]
    return df_cleaned

def remove_rows_with_nulls(df):
    # Drop rows with only null values
    df_cleaned = df.dropna(axis=0, how='all')
    return df_cleaned

def agregar_columna_condicional(df):
    # Crear una nueva columna basada en la condición de 'Nº Stro.'
    df['Siniestro'] = df['Nº Stro.'].apply(lambda x: 1 if x > 0 else 0)
    return df

def eliminar_filas_condicionales(df):
    # Crear la nueva columna
    df['Siniestro'] = df['Nº Stro.'].apply(lambda x: 1 if x > 0 else 0)
    
    # Eliminar filas donde 'Nueva_Columna' es igual a 0
    df_filtrado = df[df['Siniestro'] != 0].copy()
    
    # Eliminar la columna temporal 'Nueva_Columna'
    df_filtrado = df_filtrado.drop('Siniestro', axis=1)
    
    return df_filtrado

def vincular_etiquetas(df, columnas_codigo_etiqueta):
    """
    Vincula códigos con sus etiquetas en un DataFrame.

    Parámetros:
    - df: DataFrame original.
    - columnas_codigo_etiqueta: Lista de pares de columnas (código, etiqueta) a vincular.

    Retorna:
    - DataFrame modificado con las nuevas columnas de etiquetas.
    """
    df_modificado = df.copy()

    for codigo_col, etiqueta_col in columnas_codigo_etiqueta:
        # Crear un diccionario de mapeo de código a etiqueta
        mapeo_codigo_etiqueta = dict(zip(df[codigo_col], df[etiqueta_col]))

        # Crear una nueva columna de etiquetas basada en el código
        df_modificado[f'{codigo_col}_etiqueta'] = df_modificado[codigo_col].map(mapeo_codigo_etiqueta)

    return df_modificado

def data_exploration(df):
    # Display basic statistics of the numerical columns
    print("Basic Statistics:")
    print(df.describe())

    # Display the distribution of the 'Siniestro' column
    plt.figure(figsize=(8, 6))
    sns.countplot(x='Siniestro', data=df)
    plt.title('Distribution of Claims')
    plt.xlabel('Claim Status')
    plt.ylabel('Count')
    plt.show()

    # Display correlations between numerical features
    plt.figure(figsize=(12, 10))
    correlation_matrix = df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
    plt.title('Correlation Matrix')
    plt.show()

    # Display pair plots to visualize relationships between numerical features
    sns.pairplot(df, hue='Siniestro', palette='Set1')
    plt.suptitle('Pair Plot of Numerical Features by Claim Status', y=1.02)
    plt.show()

# Example of usage:
# data_exploration(your_dataframe)

