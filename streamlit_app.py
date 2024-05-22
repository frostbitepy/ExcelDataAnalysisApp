import streamlit as st
import pandas as pd
import locale
from config_variables import products_dict
from produccion_handler import procesar_produccion, sumar_rrc, sumar_rrc_sin_servicio, cantidad_produccion
from siniestros_handler import procesar_siniestros, sumar_siniestros, cantidad_siniestros
from filters import filter_products, filter_via_importacion, filter_capitales, filter_year, capital_filter, year_filter
from preprocessing import to_excel


def main():
    """
    Main function of the Streamlit app.
    """

    # FILTROS
    # st.sidebar.title("Filtros")
    # valid_products_selection = filter_products(products_dict)
    # via_importacion_list = filter_via_importacion()
    # min_val, max_val = filter_capitales()
    # min_year, max_year = filter_year()    

   
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

        
        # if min_val and max_val:
            # produccion_df = capital_filter(produccion_df, min_val, max_val, 'Auto Cober. Básica 1')
            # siniestro_df = capital_filter(siniestro_df, min_val, max_val, 'Auto Cober. Básica 1')

        # if min_year and max_year:
            # produccion_df = year_filter(produccion_df, min_year, max_year, 'Año')
            # siniestro_df = year_filter(siniestro_df, min_year, max_year, 'Año')
        

        produccion_results = procesar_produccion(produccion_df, fecha_inicio_corte, fecha_fin_corte)  
        siniestros_results = procesar_siniestros(siniestro_df)

        if produccion_results is not None and siniestros_results is not None:
            # Crear un botón en Streamlit llamado "Generar informe"
            if st.button("Generar informe"):
                # Variables iniciales
                valor_produccion = sumar_rrc(produccion_results)
                valor_produccion_sin_servicio = sumar_rrc_sin_servicio(produccion_results)
                siniestros = sumar_siniestros(siniestros_results)
                
                produccion_df = produccion_results
                siniestro_df = siniestros_results

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
                st.dataframe(df_prima, hide_index=True)
                st.dataframe(df_prima_tecnica, hide_index=True)

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
                st.dataframe(produccion_df, use_container_width=True, hide_index=True)

                # Create a download button for the Excel data
                st.download_button(
                    label="Download data as Excel",
                    data=excel_data,
                    file_name='data.xlsx',
                    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )



if __name__ == "__main__":
    main()