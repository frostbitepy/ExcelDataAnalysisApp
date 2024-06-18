import streamlit as st
import pandas as pd
from io import BytesIO
from produccion_handler import (
    procesar_produccion, 
    cantidad_produccion, 
)
from siniestros_handler import (
    procesar_siniestros, 
)
from filters import (
    apply_filters,
    apply_capital_filters,
    generate_results
)  
from preprocessing import (
    eliminar_filas_por_valor,
    generate_and_download_excel,
    to_excel
)


def main():
    """
    Main function of the Streamlit app.
    """
 
    # Center elements
    st.title("Informes por ejercicio")

    fecha_inicio_corte = st.date_input("Fecha de Inicio Corte", value=pd.to_datetime('today'))
    fecha_fin_corte = st.date_input("Fecha de Fin Corte", value=pd.to_datetime('today'))
    

    @st.cache
    def cargar_datos(uploaded_file):
        if uploaded_file:
            with st.spinner("Loading data..."):
                df = pd.read_excel(uploaded_file)
            # st.success("Data loaded successfully!")
            return df
        else:
            return None
        
    @st.cache_data
    def convert_dict_to_excel(data_dict):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            workbook = writer.book

            cell_format = workbook.add_format({'text_wrap': False})

            for key, value_list in data_dict.items():
                sheet_name = str(key)

                for i, item in enumerate(value_list):
                    sheet_name_item = sheet_name
                
                    item.to_excel(writer, sheet_name=sheet_name_item, index=False, startrow=i * (len(item) + 10), header=True)
                
                    for j, column in enumerate(item.columns):
                        max_len = max(item[column].astype(str).apply(len).max(), len(column))
                        writer.sheets[sheet_name_item].set_column(j, j, max_len + 2, cell_format)

            writer.save()  # Don't forget to save the ExcelWriter object

        processed_data = output.getvalue()
        return processed_data

    # Upload Produccion Excel file
    uploaded_produccion_file = st.file_uploader("Cargar planilla de producción", type=["xlsx"])
    # Upload Siniestros Excel file
    uploaded_siniestro_file = st.file_uploader("Cargar planilla de siniestros", type=["xlsx"])

    # Initialize variable to track if both files are uploaded
    both_files_uploaded = False 

    # Load production data
    produccion_df = cargar_datos(uploaded_produccion_file)
    
    if produccion_df is not None:
        st.success("Data loaded successfully!")
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
        # Apply filters
        produccion_df, siniestro_df = apply_filters(produccion_df, siniestro_df)

        # Add a selectbox to let the user choose whether to apply multiple capital filters
        st.sidebar.title("Filtro de Capitales")
        apply_multiple_filters = st.sidebar.selectbox("Aplicar filtro por Capitales?", ["No", "Yes"])

        # Initialize two empty lists to store the results
        df_prima_list = []
        df_prima_tecnica_list = []
        
        if apply_multiple_filters == "Yes":
            filtered_dfs = apply_capital_filters(produccion_df, siniestro_df)

        if st.button("Generar Reporte"):
            if apply_multiple_filters == "Yes":
                # filtered_dfs = apply_capital_filters(produccion_df, siniestro_df)

                # For each filtered dataframe, process and display the results
                for i, (filtered_produccion_df, filtered_siniestro_df) in enumerate(filtered_dfs):
                    # Process production and claims data
                    with st.spinner("Generating..."):
                        produccion_results = procesar_produccion(filtered_produccion_df, fecha_inicio_corte, fecha_fin_corte)  
                        siniestros_results = procesar_siniestros(filtered_siniestro_df)

                    # Generate the results and store them in the lists
                    df_prima = generate_results(produccion_results, siniestros_results, cantidad_emitidos)[0]
                    df_prima_tecnica = generate_results(produccion_results, siniestros_results, cantidad_emitidos)[1]
                    df_prima_list.append(df_prima)
                    df_prima_tecnica_list.append(df_prima_tecnica)
            else:
                # Process production and claims data
                with st.spinner("Generating..."):
                    produccion_results = procesar_produccion(produccion_df, fecha_inicio_corte, fecha_fin_corte)  
                    siniestros_results = procesar_siniestros(siniestro_df)

                # Generate the results
                df_prima = generate_results(produccion_results, siniestros_results, cantidad_emitidos)[0]
                df_prima_tecnica = generate_results(produccion_results, siniestros_results, cantidad_emitidos)[1]
                df_prima_list.append(df_prima)
                df_prima_tecnica_list.append(df_prima_tecnica)
    
            # Concatenate all the DataFrames in the lists into single DataFrames
            final_df_prima = pd.concat(df_prima_list, axis=0)
            final_df_prima_tecnica = pd.concat(df_prima_tecnica_list, axis=0)

            # Reset the index of the DataFrames
            final_df_prima.reset_index(drop=True, inplace=True)
            final_df_prima_tecnica.reset_index(drop=True, inplace=True)

            # Display the final DataFrames
            st.subheader("Prima")
            st.dataframe(final_df_prima)
            st.subheader("Prima Técnica")
            st.dataframe(final_df_prima_tecnica)

            # Create a dictionary with the dataframes
            data_dict = {
                'Produccion': [produccion_df],
                'Siniestros': [siniestro_df],
                'Prima': [final_df_prima],
                'Prima Tecnica': [final_df_prima_tecnica]
            }

            # Convert the dictionary to Excel data
            excel_data = convert_dict_to_excel(data_dict)

            # Create a download button for the Excel data
            st.download_button(
                label="Descargar resumen en Excel",
                data=excel_data,
                file_name='Resumen.xlsx',
                mime='text/xlsx'
            )
                
if __name__ == "__main__":
    main()


