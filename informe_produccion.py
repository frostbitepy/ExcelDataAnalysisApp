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


def main():
    st.title("Informes por ejercicio")

    fecha_inicio_corte = st.date_input("Fecha de Inicio Corte", value=pd.to_datetime('today'))
    fecha_fin_corte = st.date_input("Fecha de Fin Corte", value=pd.to_datetime('today'))

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

    # Load production data
    produccion_df = cargar_datos(uploaded_produccion_file)

    produccion_results = procesar_produccion(produccion_df, fecha_inicio_corte, fecha_fin_corte)  

    if produccion_results:
            # Crear un botón en Streamlit llamado "Generar informe"
            if st.button("Generar informe"):
                # Variables iniciales
                valor_produccion = produccion_results['suma_rrc']
                valor_produccion_sin_servicio = produccion_results['suma_rrc_sin_servicio']
                
                produccion_df = produccion_results['df']

                # Convertir siniestros y valor_produccion a tipos numéricos si es posible
                valor_produccion = pd.to_numeric(valor_produccion, errors='coerce')
                valor_produccion_sin_servicio = pd.to_numeric(valor_produccion_sin_servicio, errors='coerce')


                # Set the locale to your desired format (e.g., Spanish)
                locale.setlocale(locale.LC_NUMERIC, 'es_ES.UTF-8')  # Adjust the locale as needed

                st.write("Valor de producción: ", locale.format('%.2f', valor_produccion, grouping=True))
                st.write("Valor de producción sin servicio: ", locale.format('%.2f', valor_produccion_sin_servicio, grouping=True))



if __name__ == "__main__":
    main()