import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
    st.title("Excel Data Analysis App")

    # Upload Excel file
    uploaded_file = st.file_uploader("Upload Excel file", type=["xlsx"])

    if uploaded_file:
        # Show loading spinner
        with st.spinner("Loading data..."):
            df = read_excel(uploaded_file)

        # Display first few rows of the DataFrame
        st.success("Data loaded successfully!")
        st.dataframe(df.head())
        # Filters
        st.header("Filters")
        filters = {}
        for col in df.columns:
            filters[col] = st.text_input(f"Enter value for {col} (leave blank for all):", "")

        # Show total sum
        total_sum = df['Stro. Auto Cobertura Básica 1'].astype(float).sum()
        st.write(f"Total Sum of 'Stro. Auto Cobertura Básica 1': {total_sum}")

        # Chart Type
        chart_type = st.selectbox("Select the type of chart:", ["Line Chart", "Bar Chart", "Scatter Chart"])

        # Action button to display chart
        if st.button("Display Chart"):
            st.header("Chart")
            display_chart(df, filters, chart_type)

if __name__ == "__main__":
    main()