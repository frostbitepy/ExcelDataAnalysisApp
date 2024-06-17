import pandas as pd
import streamlit as st
import io

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


def eliminar_filas_por_valor(df, columna, valor_a_eliminar):
    """
    Elimina las filas del DataFrame donde la columna tiene el valor especificado.

    Parameters:
    - df: DataFrame
    - columna: str, nombre de la columna en la que buscar
    - valor_a_eliminar: str o list, valor o lista de valores a eliminar

    Returns:
    - DataFrame modificado
    """
    if isinstance(valor_a_eliminar, str):
        # Si valor_a_eliminar es un solo valor, conviértelo a una lista
        valor_a_eliminar = [valor_a_eliminar]

    # Filtra el DataFrame para mantener solo las filas donde la columna no contiene los valores especificados
    df_filtrado = df[~df[columna].isin(valor_a_eliminar)]

    return df_filtrado

# Ejemplo de uso:
# Supongamos que df es tu DataFrame
# Reemplaza 'Nombre Tipo Póliza_etiqueta' con el nombre real de la columna
# y 'Anulacion' con el valor que deseas eliminar
# df = eliminar_filas_por_valor(df, 'Nombre Tipo Póliza_etiqueta', 'Anulacion')

# Crear una función que reciba un dataframe, una columna y devuelva los valores unicos de la columna en una lista
def unique_values(df, column):
    unique_values = df[column].unique().tolist()
    return unique_values

# Crear una funcion que reciba un dataframe, una columna y una lista de valores, 
# devuelve el dataframe luego de haber elimiado las filas que no contengan los valores de la lista en la columna especificada
def filter_values(df, column, values):
    df_filtered = df[df[column].isin(values)]
    return df_filtered


def suma_columna(dataframe, nombre_columna):
    # Verificar si la columna existe en el dataframe
    if nombre_columna not in dataframe.columns:
        return f"La columna '{nombre_columna}' no existe en el dataframe."

    # Calcular la suma de los valores en la columna
    suma = dataframe[nombre_columna].sum()
    return suma

# Ejemplo de uso
# Supongamos que tienes un dataframe llamado 'mi_dataframe' y una columna 'mi_columna'
# Puedes llamar a la función de la siguiente manera:
# resultado = suma_columna(mi_dataframe, 'mi_columna')
# print(resultado)

# Funcion que recibe dos parametros, un dataframe y el nombre de una columna, eliminar los valores null de esa columna
def eliminar_nulls(dataframe, nombre_columna):
    # Verificar si la columna existe en el dataframe
    if nombre_columna not in dataframe.columns:
        return f"La columna '{nombre_columna}' no existe en el dataframe."

    # Eliminar los valores null, NaN y 0 de la columna
    dataframe = dataframe[dataframe[nombre_columna].notnull()]
    dataframe = dataframe[dataframe[nombre_columna] != 0]
    return dataframe



def to_excel(df):
    """
    Write a DataFrame to an Excel file and return it as a bytes object.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Resumen', index=False)
    excel_data = output.getvalue()
    return excel_data


def get_unique_values(df, column_name):
    unique_values = df[column_name].unique().tolist()
    return unique_values


def generate_and_download_excel(produccion_df, siniestro_df):
    with st.spinner("Generating Excel file..."):
        # Convert the Dataframe to excel
        excel_data = to_excel(produccion_df)

    # Columnas a mostrar
    columns_to_show = ['Nombre Producto','Via Importación','Prima Art.','Fec. Desde Art.','Fec. Hasta Art.','Plazo','Devengado','RRC']
    produccion_df = produccion_df[columns_to_show]

    # Display the count of rows for the "Produccion" DataFrame
    st.write("Cantidad Produccion:", produccion_df.shape[0])

    # Display the count of rows for the "Siniestros" DataFrame
    st.write("Cantidad Siniestros:", siniestro_df.shape[0]) 

    # Mostrar dataframe
    # st.dataframe(produccion_df, use_container_width=True, hide_index=True)

    # Create a download button for the Excel data
    st.download_button(
        label="Download data as Excel",
        data=excel_data,
        file_name='data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

def to_excel_file(df):
    """
    Write a DataFrame to an Excel file and return it as a bytes object.
    """
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Resumen', index=False)
        writer.save()  # Call 'save' on the 'ExcelWriter' object
    excel_data = output.getvalue()
    return excel_data