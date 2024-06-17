import streamlit as st
import pandas as pd
import locale
from config_variables import product_to_capital
from config_variables import filter_dict    
from babel.numbers import format_decimal
from produccion_handler import (
    sumar_rrc, 
    sumar_rrc_sin_servicio, 
    sumar_capital_asegurado
)
from siniestros_handler import (
    sumar_siniestros
)


def capital_filter(dataframe, min_val, max_val):
    """
    Filter a DataFrame based on a condition.
    
    Parameters:
    dataframe (pandas.DataFrame): The DataFrame to filter.
    min_val (float): The minimum value of the range.
    max_val (float): The maximum value of the range.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """

    # Create an empty DataFrame to store the filtered rows
    filtered_df = pd.DataFrame()

    # Loop over each product and its corresponding capital column
    for product, capital_column in product_to_capital.items():
        # Filter the DataFrame for rows where 'products' is equal to the current product
        product_df = dataframe[dataframe['Nombre Producto'] == product]
        
        # Apply the range filter to the capital column of the filtered DataFrame
        product_filtered_df = product_df[(product_df[capital_column] >= min_val) & (product_df[capital_column] <= max_val)]
        
        # Append the filtered rows to the final DataFrame
        filtered_df = pd.concat([filtered_df, product_filtered_df])

    # If the filtered DataFrame is empty, return a message indicating no values in the range
    if filtered_df.empty:
        return f"No values in the range {min_val} to {max_val} in the capital columns."

    return filtered_df



def year_filter(dataframe, min_year, max_year, column):
    """
    Filter a DataFrame based on a range of years.

    Parameters:
    dataframe (pandas.DataFrame): The DataFrame to filter.
    min_year (int): The minimum year of the range.
    max_year (int): The maximum year of the range.
    column (str): The column to apply the condition on.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """

    # Use the boolean indexing feature of pandas to filter the DataFrame
    filtered_df = dataframe[(dataframe[column] >= min_year) & (dataframe[column] <= max_year)]

    # If the filtered DataFrame is empty, return a message indicating no values in the range
    if filtered_df.empty:
        return f"No values in the range {min_year} to {max_year} in the column '{column}'."

    return filtered_df


def get_unique_values(df, column_name):
    unique_values = df[column_name].unique().tolist()
    return unique_values


def apply_filters(df1, df2):
    # Select filters
    st.sidebar.title("Filtros")

    # For each filter, display a checkbox in the sidebar
    selected_filters = []
    for filter in filter_dict.keys():
        if st.sidebar.checkbox(f"{filter}"):
            selected_filters.append(filter)

    # For each selected filter, display a multiselect widget with the unique values of the corresponding column
    for filter in selected_filters:
        column_name = filter_dict[filter]
        unique_values_df1 = get_unique_values(df1, column_name)
        unique_values_df2 = get_unique_values(df2, column_name)
        unique_values = list(set(unique_values_df1 + unique_values_df2))

        # Remove empty values
        unique_values = [value for value in unique_values if value and not pd.isna(value)]

        selected_values = st.sidebar.multiselect(f"Selecciona valores para {filter}", unique_values)

        # Filter the DataFrames based on the selected values, if any
        if selected_values:
            df1 = df1[df1[column_name].isin(selected_values)]
            df2 = df2[df2[column_name].isin(selected_values)]
    
    return df1, df2


def apply_capital_filters(df1, df2):
    # Ask the user for the number of capital filters to apply
    num_filters = st.sidebar.slider("Numero de filtros por Capitales", min_value=0, max_value=10, value=0)

    # Initialize a list to store the filtered dataframes
    filtered_dfs = []

    # Initialize the las max value
    last_max_val = 0.0

    # For each filter, display two input fields for the min and max capital values
    for i in range(num_filters):
        min_val = st.sidebar.number_input(f"Capital mínimo para filtro {i+1}", value=last_max_val + 1.0)
        max_val = st.sidebar.number_input(f"Capital máximo para filtro {i+1}", value=0.0)
        st.sidebar.write("___________")

        # Strore the max value for the next iteration
        last_max_val = max_val

        # Apply the capital filter to the dataframes
        filtered_df1 = capital_filter(df1, min_val, max_val)
        filtered_df2 = capital_filter(df2, min_val, max_val)

        # Check if the returned objects are dataframes
        if isinstance(filtered_df1, pd.DataFrame) and isinstance(filtered_df2, pd.DataFrame):
            # Format min_val and max_val with thousands separators
            min_val_str = "{:,.0f}".format(min_val).replace(",", ".")
            max_val_str = "{:,.0f}".format(max_val).replace(",", ".")

            # Add a new column at the beginning of the filtered dataframes to indicate the capital range
            for df in [filtered_df1, filtered_df2]:
                df.insert(0, 'Rango de Capitales', f"{min_val_str} - {max_val_str}")
        else:
            st.error("Debe ingresar todos los rangos de capitales.")

        # Add the filtered dataframes to the list
        filtered_dfs.append((filtered_df1, filtered_df2))

    return filtered_dfs


def generate_results(produccion_results, siniestros_results, cantidad_emitidos):
    if produccion_results is not None and siniestros_results is not None:
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
        emitidos = locale.format('%.0f', cantidad_emitidos, grouping=True)
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



        if "Rango de Capitales" in produccion_df.columns:
            rango_capitales = produccion_df['Rango de Capitales'].iloc[0]
            # Crear datos para la tabla
            data_prima = {
                "Rango de Capitales": [rango_capitales],
                "Cantidad Devengado": [format_number_es(cantidad_devengado)],
                "Suma Asegurada Art.": [format_number_es(suma_asegurada)],
                "Promedio Suma Asegurada": [format_number_es(suma_asegurada_promedio)],
                "Prima Devengada": [format_number_es(prima_devengada)],
                "Prima Promedio": [format_number_es(prima_promedio)],
                "Frecuencia": [format_number_es(frecuencia)], 
                "Intensidad": [format_number_es(intensidad)],
                "Cantidad Siniestros": [format_number_es(cantidad_siniestros)],
                "Sumatoria Siniestros": [format_number_es(suma_siniestros)],
                "Siniestros/Produccion": [format_number_es(porcentaje_siniestros)]
            }

            data_prima_tecnica = {
                "Rango de Capitales": [rango_capitales],
                "Cantidad Devengado": [format_number_es(cantidad_devengado)],
                "Suma Asegurada Art.": [format_number_es(suma_asegurada)],
                "Promedio Suma Asegurada": [format_number_es(suma_asegurada_promedio)],
                "Prima Técnica Devengada": [format_number_es(prima_tecnica_devengada)],
                "Prima Promedio": [format_number_es(prima_tecnica_promedio)],
                "Frecuencia": [format_number_es(frecuencia)],
                "Intensidad": [format_number_es(intensidad)],
                "Cantidad Siniestros": [format_number_es(cantidad_siniestros)],
                "Sumatoria Siniestros": [format_number_es(suma_siniestros)],
                "Siniestros/Produccion": [format_number_es(porcentaje_siniestros_sin_servicio)]
            }
        
        else:
            # Crear datos para la tabla
            data_prima = {
                # "Cantidad Emitido": [emitidos],
                "Cantidad Devengado": [format_number_es(cantidad_devengado)],
                "Suma Asegurada Art.": [format_number_es(suma_asegurada)],
                "Promedio Suma Asegurada": [format_number_es(suma_asegurada_promedio)],
                "Prima Devengada": [format_number_es(prima_devengada)],
                "Prima Promedio": [format_number_es(prima_promedio)],
                "Frecuencia": [format_number_es(frecuencia)], 
                "Intensidad": [format_number_es(intensidad)],
                "Cantidad Siniestros": [format_number_es(cantidad_siniestros)],
                "Sumatoria Siniestros": [format_number_es(suma_siniestros)],
                "Siniestros/Produccion": [format_number_es(porcentaje_siniestros)]
            }

            data_prima_tecnica = {
                # "Cantidad Emitido": [emitidos],
                "Cantidad Devengado": [format_number_es(cantidad_devengado)],
                "Suma Asegurada Art.": [format_number_es(suma_asegurada)],
                "Promedio Suma Asegurada": [format_number_es(suma_asegurada_promedio)],
                "Prima Técnica Devengada": [format_number_es(prima_tecnica_devengada)],
                "Prima Promedio": [format_number_es(prima_tecnica_promedio)],
                "Frecuencia": [format_number_es(frecuencia)],
                "Intensidad": [format_number_es(intensidad)],
                "Cantidad Siniestros": [format_number_es(cantidad_siniestros)],
                "Sumatoria Siniestros": [format_number_es(suma_siniestros)],
                "Siniestros/Produccion": [format_number_es(porcentaje_siniestros_sin_servicio)]
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
        # st.subheader("Prima")
        # st.markdown(df_prima_html, unsafe_allow_html=True)
        # st.subheader("Prima Técnica")
        # st.markdown(df_prima_tecnica_html, unsafe_allow_html=True)

        # Return a list of dataframe objects
        return [df_prima, df_prima_tecnica]


def format_number_es(number):
    return format_decimal(number, locale='es_ES')

