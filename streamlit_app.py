import streamlit as st
import pandas as pd
import locale
from config_variables import products_dict
from produccion_handler import (
    procesar_produccion, 
    sumar_rrc, 
    sumar_rrc_sin_servicio, 
    cantidad_produccion, 
    sumar_capital_asegurado
)
from siniestros_handler import (
    procesar_siniestros, 
    sumar_siniestros, 
    cantidad_siniestros
)
from filters import (
    filter_products,
    filter_via_importacion,
    filter_capitales,
    filter_year,
    capital_filter, 
    year_filter, 
    apply_filters,
    apply_capital_filters,
    display_results
)  
from preprocessing import (
    to_excel, 
    eliminar_filas_por_valor
)


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

        # Add a selectbox to let the user choose whether to apply multiple capital filters
        st.sidebar.title("Filtro de Capitales")
        apply_multiple_filters = st.sidebar.selectbox("Aplicar filtro por Capitales?", ["No", "Yes"])
        
        if apply_multiple_filters == "Yes":
            filtered_dfs = apply_capital_filters(produccion_df, siniestro_df)

        if st.button("Generar Reporte"):
            if apply_multiple_filters == "Yes":
                # filtered_dfs = apply_capital_filters(produccion_df, siniestro_df)

                # For each filtered dataframe, process and display the results
                for i, (filtered_produccion_df, filtered_siniestro_df) in enumerate(filtered_dfs):
                    st.subheader(f"Rango de Capitales {i+1}")

                    # Process production and claims data
                    with st.spinner("Generating..."):
                        produccion_results = procesar_produccion(filtered_produccion_df, fecha_inicio_corte, fecha_fin_corte)  
                        siniestros_results = procesar_siniestros(filtered_siniestro_df)

                    # Display the results
                    display_results(produccion_results, siniestros_results, cantidad_emitidos)
            else:
                # Process production and claims data
                with st.spinner("Generating..."):
                    produccion_results = procesar_produccion(produccion_df, fecha_inicio_corte, fecha_fin_corte)  
                    siniestros_results = procesar_siniestros(siniestro_df)

                # Display the results
                display_results(produccion_results, siniestros_results, cantidad_emitidos)

                
if __name__ == "__main__":
    main()


