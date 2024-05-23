import streamlit as st
import pandas as pd
from config_variables import product_to_capital
from config_variables import filter_dict    

def filter_products(products_dict):
    st.sidebar.subheader("Productos")
    valid_products_selection = st.sidebar.multiselect(
        'Selecciona los productos a incluir en el informe:', products_dict.keys()
    )
    return valid_products_selection

def filter_via_importacion():
    st.sidebar.subheader("Vía Importación")
    representante = st.sidebar.checkbox('REPRESENTANTE',value=True)
    via_chile = st.sidebar.checkbox('VIA CHILE',value=True)
    otros = st.sidebar.checkbox('OTROS',value=True)

    via_importacion_list = [''] * 3
    if representante:
        via_importacion_list[0] = 'REPRESENTANTE'
    if via_chile:
        via_importacion_list[1] = 'VIA CHILE'
    if otros:
        via_importacion_list[2] = 'OTROS'
    return via_importacion_list

def filter_capitales():
    st.sidebar.subheader("Filtro por Capitales")
    range_filter = st.sidebar.checkbox('Aplicar filtro por capitales')
    min_val, max_val = 0, None
    if range_filter:
        min_val = st.sidebar.number_input('Enter minimum value')
        max_val = st.sidebar.number_input('Enter maximum value')
    return min_val, max_val

def filter_year():
    st.sidebar.subheader("Filtro por Año del Vehículo")
    year_range = st.sidebar.checkbox('Aplicar filtro por Año')
    min_year, max_year = None, None
    if year_range:
        min_year = st.sidebar.number_input('Enter minimum value')
        max_year = st.sidebar.number_input('Enter maximum value')
    return min_year, max_year


def deprecated_capital_filter(dataframe, min_val, max_val, column):
    """
    Filter a Dataframe based on a condition.
    
    Parameters:
    df (pandas.DataFrame): The DataFrame to filter.
    min_val (float): The minimum value of the range.
    max_val (float): The maximum value of the range.
    column (str): The columns to apply the condition on.

    Returns:
    pandas.DataFrame: The filtered DataFrame.
    """

    # Use the boolean indexing feature of pandas to filter the Dataframe
    filtered_df = dataframe[(dataframe[column] >= min_val) & (dataframe[column] <= max_val)]

    # If the filtered DataFrame is empty, return a message indicating no values in the range
    if filtered_df.empty:
        return f"No values in the range {min_val} to {max_val} in the column '{column}'."

    return filtered_df


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
    # selected_filters = st.sidebar.multiselect("Select filters", list(filter_dict.keys()))

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
        selected_values = st.sidebar.multiselect(f"Select values for {filter}", unique_values)

        # Filter the DataFrames based on the selected values, if any
        if selected_values:
            df1 = df1[df1[column_name].isin(selected_values)]
            df2 = df2[df2[column_name].isin(selected_values)]
    
    return df1, df2