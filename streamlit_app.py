import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import locale
from datetime import datetime, timedelta
from produccion_handler import procesar_produccion
from siniestros_handler import procesar_siniestros
from preprocessing import capital_filter, year_filter 


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
    'OTROS': 3
}

via_importacion_list = ['REPRESENTANTE','VIA CHILE','OTROS']


def main():

    # Sidebar elements
    st.sidebar.title("Filtros")

    st.sidebar.subheader("Productos")
    # Using object notation
    valid_products_selection = st.sidebar.multiselect(
        'Selecciona los productos a incluir en el informe:', products_dict.keys()
        )
       
    # st.sidebar.write('You selected:', valid_products_selection)

    # vía importación # CHECK THIS OUT
    st.sidebar.subheader("Vía Importación")
    representante = st.sidebar.checkbox('REPRESENTANTE',value=True)
    via_chile = st.sidebar.checkbox('VIA CHILE',value=True)
    otros = st.sidebar.checkbox('OTROS',value=True)

    if representante:
        via_importacion_list[0] = 'REPRESENTANTE'
    else:
        via_importacion_list[0] = ''
    
    if via_chile:
        via_importacion_list[1] = 'VIA CHILE'
    else:
        via_importacion_list[1] = ''
    
    if otros:
        via_importacion_list[2] = 'OTROS'
    else:
        via_importacion_list[2] = ''


    st.sidebar.subheader("Filtro por Capitales")
    # Add a checkbox to the sidebar
    range_filter = st.sidebar.checkbox('Aplicar filtro por capitales')

    # If the checkbox is checked, display two text fields for entering the minimum and maximum values
    if range_filter:
        min_val = st.sidebar.number_input('Enter minimum value')
        max_val = st.sidebar.number_input('Enter maximum value')

        # Display the formated number
        if min_val:
            st.sidebar.markdown(f"Minimum value: {int(min_val):,}".replace(",", "."))
        if max_val:
            st.sidebar.markdown(f"Maximum value: {int(max_val):,}".replace(",", "."))
    
    else:
        min_val = None
        max_val = None



    st.sidebar.subheader("Filtro por Año del Vehículo")
    # Add a checkbox to the sidebar
    year_range = st.sidebar.checkbox('Aplicar filtro por Año')

    # If the checkbox is checked, display two text fields for entering the minimum and maximum values
    if year_range:
        min_year = st.sidebar.number_input('Enter minimum value')
        max_year = st.sidebar.number_input('Enter maximum value')

        # Display the formated number
        if min_year:
            st.sidebar.markdown(f"Minimum value: {int(min_year):,}")
        if max_year:
            st.sidebar.markdown(f"Maximum value: {int(max_year):,}")
    
    else:
        min_year = None
        max_year = None
    

   
    # Center elements
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

        if min_val and max_val:
            produccion_df = capital_filter(produccion_df, min_val, max_val, 'Suma Asegurada Art.')
            siniestro_df = capital_filter(siniestro_df, min_val, max_val, 'Suma Asegurada Art.')

        if min_year and max_year:
            produccion_df = year_filter(produccion_df, min_year, max_year, 'Año')
            siniestro_df = year_filter(siniestro_df, min_year, max_year, 'Año')
        
        produccion_results = procesar_produccion(produccion_df, fecha_inicio_corte, fecha_fin_corte, valid_products_selection, via_importacion_list)  
        siniestros_results = procesar_siniestros(siniestro_df, valid_products_selection, via_importacion_list)

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
                    "Cantidad Produccion": [locale.format('%.0f', produccion_df.shape[0], grouping=True)],
                    "Prima devengada": [locale.format('%.2f', valor_produccion, grouping=True)],
                    "Cantidad Siniestros": [locale.format('%.0f', siniestro_df.shape[0], grouping=True)],
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
                columns_to_show = ['Nombre Producto','Via Importación','Prima Art.','Fec. Desde Art.','Fec. Hasta Art.','Plazo','Devengado','RRC']
                produccion_df = produccion_df[columns_to_show]

                # Display the count of rows for the "Produccion" DataFrame
                st.write("Cantidad Produccion:", produccion_df.shape[0])

                # Display the count of rows for the "Siniestros" DataFrame
                st.write("Cantidad Siniestros:", siniestro_df.shape[0]) 

                # Mostrar dataframe
                st.dataframe(produccion_df)



if __name__ == "__main__":
    main()