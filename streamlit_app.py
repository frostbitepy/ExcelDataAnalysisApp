import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import locale
from datetime import datetime, timedelta
from produccion_handler import procesar_produccion
from siniestros_handler import procesar_siniestros


def read_excel(file):
    df = pd.read_excel(file, engine='openpyxl', dtype=str)
    return df

def apply_filters(df, filters):
    # Apply filters based on user input
    for col, value in filters.items():
        df = df[df[col] == value]
    return df

def display_chart(df, filters, chart_type):
    # Apply filters if any
    filtered_df = apply_filters(df, filters)

    # Get column for x-axis
    column_name = st.selectbox("Select the column for the x-axis:", filtered_df.columns)

    # Choose the type of chart
    if chart_type == "Line Chart":
        st.line_chart(filtered_df[[column_name, 'Stro. Auto Cobertura Básica 1']])
    elif chart_type == "Bar Chart":
        st.bar_chart(filtered_df[[column_name, 'Stro. Auto Cobertura Básica 1']])
    elif chart_type == "Scatter Chart":
        st.scatter_chart(filtered_df[[column_name, 'Stro. Auto Cobertura Básica 1']])

def main():
    st.title("Informes por ejercicio")

    fecha_inicio_corte = st.date_input("Fecha de Inicio Corte", value=pd.to_datetime('today'))
    fecha_fin_corte = st.date_input("Fecha de Fin Corte", value=pd.to_datetime('today'))


    @st.cache_data
    def cargar_datos(uploaded_file):
        if uploaded_file:
            with st.spinner("Loading data..."):
                df = pd.read_excel(uploaded_file)
            st.success("Data loaded successfully!")
            return df
        else:
            return None

    # Upload Produccion Excel file
    uploaded_produccion_file = st.file_uploader("Cargar planilla de producción", type=["xlsx"])
    # Upload Siniestros Excel file
    uploaded_siniestro_file = st.file_uploader("Cargar planilla de siniestros", type=["xlsx"])

    # Initialize variable to track if both files are uploaded
    both_files_uploaded = False 

    # Load production data
    produccion_df = cargar_datos(uploaded_produccion_file)

    # Load siniestro data
    siniestro_df = cargar_datos(uploaded_siniestro_file)

    # Check if both files are uploaded before proceeding
    if produccion_df is not None and siniestro_df is not None:
        both_files_uploaded = True

    # Check if both files are uploaded before proceeding
    if both_files_uploaded:
        
        produccion_results = procesar_produccion(produccion_df, fecha_inicio_corte, fecha_fin_corte)  
        siniestros_results = procesar_siniestros(siniestro_df)

        if produccion_results is not None and siniestros_results is not None:
            # Crear un botón en Streamlit llamado "Generar informe"
            if st.button("Generar informe"):
                # Variables iniciales
                valor_produccion = produccion_results['suma_rrc']
                valor_produccion_sin_servicio = produccion_results['suma_rrc_sin_servicio']
                siniestros = siniestros_results['sumatoria_siniestros']             
                
                produccion_df = produccion_results['df']
                siniestro_df = siniestros_results['df']

                # Convertir siniestros y valor_produccion a tipos numéricos si es posible
                siniestros = pd.to_numeric(siniestros, errors='coerce')
                valor_produccion = pd.to_numeric(valor_produccion, errors='coerce')
                valor_produccion_sin_servicio = pd.to_numeric(valor_produccion_sin_servicio, errors='coerce')

                # Calcular el porcentaje de siniestros/valor_produccion
                porcentaje_siniestros = round((siniestros / valor_produccion) * 100, 2)
                porcentaje_siniestros = str(porcentaje_siniestros) + "%"

                # Calcular el porcentaje de siniestros/valor_produccion sin servicio
                porcentaje_siniestros_sin_servicio = round((siniestros / valor_produccion_sin_servicio) * 100, 2)
                porcentaje_siniestros_sin_servicio = str(porcentaje_siniestros_sin_servicio) + "%"

                # Set the locale to your desired format (e.g., Spanish)
                locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')  # Adjust the locale as needed

                # Crear datos para la tabla
                data_prima = {
                    "Prima devengada": [locale.format('%.2f', valor_produccion, grouping=True)],
                    "Sumatoria Siniestros": [locale.format('%.2f', siniestros, grouping=True)],
                    "Siniestros/Produccion": [porcentaje_siniestros]
                }

                data_prima_tecnica = {
                    "Prima técnica devengada": [locale.format('%.2f', valor_produccion_sin_servicio, grouping=True)],
                    "Sumatoria Siniestros": [locale.format('%.2f', siniestros, grouping=True)],
                    "Siniestros/Produccion": [porcentaje_siniestros_sin_servicio]
                }

                # Crear DataFrames
                df_prima = pd.DataFrame(data_prima)
                df_prima_tecnica = pd.DataFrame(data_prima_tecnica)

                # Mostrar la tablas
                st.table(df_prima)
                st.table(df_prima_tecnica)

                # Columnas a mostrar
                columns_to_show = ['Prima Técnica Art.','Prima Art.','Fec. Desde Art.','Fec. Hasta Art.','Plazo','Devengado','RRC Unidad','RRC sin servicio','RRC']
                produccion_df = produccion_df[columns_to_show]

                # Display the count of rows for the "Produccion" DataFrame
                st.write("Cantidad Produccion:", produccion_df.shape[0])

                # Display the count of rows for the "Siniestros" DataFrame
                st.write("Cantidad Siniestros:", siniestro_df.shape[0]) 

                # Mostrar dataframe
                st.dataframe(produccion_df)
  


if __name__ == "__main__":
    main()