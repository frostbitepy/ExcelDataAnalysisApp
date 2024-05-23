import streamlit as st
import pandas as pd
import locale
from config_variables import products_dict
from produccion_handler import procesar_produccion, sumar_rrc, sumar_rrc_sin_servicio, cantidad_produccion, sumar_capital_asegurado
from siniestros_handler import procesar_siniestros, sumar_siniestros, cantidad_siniestros
from filters import filter_products, filter_via_importacion, filter_capitales, filter_year, capital_filter, year_filter, apply_filters  
from preprocessing import to_excel, eliminar_filas_por_valor


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
    
    # Eliminar filas de anulaciones de la columna 'Nombre Tipo Póliza'
    if produccion_df is not None:
        produccion_df = eliminar_filas_por_valor(produccion_df, 'Nombre Tipo Póliza', 'Anulacion') 

    if produccion_df is not None:
        cantidad_emitidos = cantidad_produccion(produccion_df)

    # Load siniestro data
    siniestro_df = cargar_datos(uploaded_siniestro_file)

    # Eliminar filas de anulaciones de la columna 'Nombre Tipo Póliza'
    if siniestro_df is not None:
        siniestro_df = eliminar_filas_por_valor(siniestro_df, 'Nombre Tipo Póliza', 'Anulacion')

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
        
        # Apply filters
        produccion_df, siniestro_df = apply_filters(produccion_df, siniestro_df)

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

                # Datos para la tabla
                emitidos = cantidad_emitidos
                cantidad_devengado = locale.format('%.0f', produccion_df.shape[0], grouping=True)
                suma_asegurada = locale.format('%.2f', sumar_capital_asegurado(produccion_df), grouping=True)
                suma_asegurada_promedio = locale.format('%.2f', sumar_capital_asegurado(produccion_df) / produccion_df.shape[0], grouping=True)
                prima_devengada = locale.format('%.2f', valor_produccion, grouping=True)
                prima_tecnica_devengada = locale.format('%.2f', valor_produccion_sin_servicio, grouping=True)
                prima_promedio = locale.format('%.2f', valor_produccion / produccion_df.shape[0], grouping=True)
                frecuencia = locale.format('%.2f', siniestro_df.shape[0] / produccion_df.shape[0], grouping=True)
                intensidad = locale.format('%.2f', siniestros / siniestro_df.shape[0], grouping=True)
                prima_tecnica_promedio = locale.format('%.2f', valor_produccion_sin_servicio / produccion_df.shape[0], grouping=True)
                suma_siniestros = locale.format('%.2f', siniestros, grouping=True)
                cantidad_siniestros = locale.format('%.0f', siniestro_df.shape[0], grouping=True)
                porcentaje_siniestros = porcentaje_siniestros
                porcentaje_siniestros_sin_servicio = porcentaje_siniestros_sin_servicio


                # Crear datos para la tabla
                data_prima = {
                    "Cantidad Emitido": [emitidos],
                    "Cantidad Devengado": [cantidad_devengado],
                    "Suma Asegurada Art.": [suma_asegurada],
                    "Promedio Suma Asegurada": [suma_asegurada_promedio],
                    "Prima devengada": [prima_devengada],
                    "Prima Promedio": [prima_promedio],
                    "Frecuencia": [frecuencia], 
                    "Intensidad": [intensidad],
                    "Cantidad Siniestros": [cantidad_siniestros],
                    "Sumatoria Siniestros": [suma_siniestros],
                    "Siniestros/Produccion": [porcentaje_siniestros]
                }

                data_prima_tecnica = {
                    "Cantidad Emitido": [emitidos],
                    "Cantidad Devengado": [cantidad_devengado],
                    "Suma Asegurada Art.": [suma_asegurada],
                    "Promedio Suma Asegurada": [suma_asegurada_promedio],
                    "Prima técnica devengada": [prima_tecnica_devengada],
                    "Prima Promedio": [prima_tecnica_promedio],
                    "Frecuencia": [frecuencia],
                    "Intensidad": [intensidad],
                    "Cantidad Siniestros": [cantidad_siniestros],
                    "Sumatoria Siniestros": [suma_siniestros],
                    "Siniestros/Produccion": [porcentaje_siniestros_sin_servicio]
                }

                # Crear DataFrames
                df_prima = pd.DataFrame(data_prima)
                df_prima_tecnica = pd.DataFrame(data_prima_tecnica)

                # Convert DataFrames to HTML without index
                df_prima_html = df_prima.to_html(index=False)
                df_prima_tecnica_html = df_prima_tecnica.to_html(index=False)

                # Wrap the HTML in a div with center alignment
                df_prima_html = f'<div style="text-align: center">{df_prima_html}</div>'
                df_prima_tecnica_html = f'<div style="text-align: center">{df_prima_tecnica_html}</div>'

                # Display the tables
                st.markdown(df_prima_html, unsafe_allow_html=True)
                st.markdown(df_prima_tecnica_html, unsafe_allow_html=True) 


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