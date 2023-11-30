import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

    # Upload Produccion Excel file
    uploaded_produccion_file = st.file_uploader("Cargar planilla de producción", type=["xlsx"])

    # Initialize variable to track if both files are uploaded
    both_files_uploaded = False 

    if uploaded_produccion_file:
        # Show loading spinner
        with st.spinner("Loading data..."):
            produccion_df = read_excel(uploaded_produccion_file)

        # Display first few rows of the DataFrame
        st.success("Data loaded successfully!")
        # st.dataframe(produccion_df.head())

    # Upload Siniestros Excel file
    uploaded_siniestro_file = st.file_uploader("Cargar planilla de siniestro", type=["xlsx"])

    if uploaded_siniestro_file:
        # Show loading spinner
        with st.spinner("Loading data..."):
            siniestro_df = read_excel(uploaded_siniestro_file)

        # Display first few rows of the DataFrame
        st.success("Data loaded successfully!")
        # st.dataframe(siniestro_df.head()) 

        # Set flag to True since both files are uploaded
        both_files_uploaded = True

    # Check if both files are uploaded before proceeding
    if both_files_uploaded:
        
        produccion_results = procesar_produccion(produccion_df, fecha_inicio_corte, fecha_fin_corte)
        siniestros_results = procesar_siniestros(siniestro_df, fecha_inicio_corte, fecha_fin_corte)
    
        # Variables iniciales
        produccion = produccion_results['sumatoria_prima_articulo']
        produccion_sin_servicio = produccion_results['sumatoria_prima_articulo_sin_servicio']
        siniestros = siniestros_results['sumatoria_siniestros']
        titulo_opciones = ["Prima técnica por artículo", "Prima por artículo"]
        selected_titulo = st.selectbox("Selecciona el tipo de prima", titulo_opciones)

        # Actualizar valor según el título seleccionado
        if selected_titulo == "Prima técnica por artículo":
            valor_produccion = produccion_sin_servicio
        elif selected_titulo == "Prima por artículo":
            valor_produccion = produccion

        # Calcular el porcentaje de siniestros/valor_produccion
        porcentaje_siniestros = (siniestros / valor_produccion) * 100
        porcentaje_siniestros = str(porcentaje_siniestros) + "%"

        # Crear datos para la tabla
        data = {
            "Prima devengada": [valor_produccion],
            "Valor": [siniestros],
            "Proporción Siniestros/Produccion": [porcentaje_siniestros]
        }

        # Crear DataFrame
        df = pd.DataFrame(data)

        # Mostrar la tabla
        st.table(df)

    

if __name__ == "__main__":
    main()