import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Read the Excel file into a DataFrame
    excel_file_path = 'SiniestrosAutomovil2022.xlsx'
    df = pd.read_excel(excel_file_path, engine='openpyxl', dtype=str)

    # Convert 'Stro. Auto Cobertura Básica 1' column to numeric
    df['Stro. Auto Cobertura Básica 1'] = pd.to_numeric(df['Stro. Auto Cobertura Básica 1'], errors='coerce')

    # Initialize filters list
    filters = []

    # Display total sum of 'Stro. Auto Cobertura Básica 1' by default
    total_sum = df['Stro. Auto Cobertura Básica 1'].sum()
    print(f"Total sum of 'Stro. Auto Cobertura Básica 1': {total_sum}")

    # Main loop for user interaction
    while True:
        print("\nOptions:")
        print("1. Add Filter")
        print("2. Remove Filter")
        print("3. Clear All Filters")
        print("4. Display Total Sum of 'Stro. Auto Cobertura Básica 1'")
        print("5. Display Graph")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_filter(df, filters)
        elif choice == '2':
            remove_filter(filters)
        elif choice == '3':
            clear_filters(filters)
        elif choice == '4':
            display_total_sum(df, filters)
        elif choice == '5':
            display_graph(df, filters)
        elif choice == '6':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

def add_filter(df, filters):
    column_name = input("Enter the column name to filter on: ")
    value = input(f"Enter the value to filter by in column '{column_name}': ")

    # Apply the filter
    filters.append((column_name, value))
    filtered_df = apply_filters(df, filters)

    # Display the filtered data
    print("\nFiltered Data:")
    print(filtered_df)

    # Display the updated total sum
    display_total_sum(filtered_df, [])

def remove_filter(filters):
    if not filters:
        print("No filters applied.")
        return

    print("Current Filters:")
    for i, (column, value) in enumerate(filters, 1):
        print(f"{i}. {column} = {value}")

    filter_index = int(input("Enter the number of the filter to remove: ")) - 1

    if 0 <= filter_index < len(filters):
        removed_filter = filters.pop(filter_index)
        print(f"Filter '{removed_filter[0]}' = '{removed_filter[1]}' removed.")
    else:
        print("Invalid filter number.")

def clear_filters(filters):
    filters.clear()
    print("All filters cleared.")

def apply_filters(df, filters):
    filtered_df = df.copy()

    for column, value in filters:
        filtered_df = filtered_df[filtered_df[column] == value]

    return filtered_df

def display_total_sum(df, filters):
    # Apply filters if any
    filtered_df = apply_filters(df, filters)

    # Display the total sum of 'Stro. Auto Cobertura Básica 1'
    total_sum = filtered_df['Stro. Auto Cobertura Básica 1'].sum()
    print(f"Total sum of 'Stro. Auto Cobertura Básica 1': {total_sum}")

def display_graph(df, filters):
    # Apply filters if any
    filtered_df = apply_filters(df, filters)

    # Get column for x-axis
    column_name = input("Enter the column name for the x-axis: ")

    if column_name in filtered_df.columns:
        # Choose the type of plot
        print("\nSelect the type of plot:")
        print("1. Scatter Plot")
        print("2. Bar Plot")
        print("3. Line Plot")

        plot_type = input("Enter your choice (1-3): ")

        if plot_type == '1':
            # Scatter plot
            plt.scatter(filtered_df[column_name], filtered_df['Stro. Auto Cobertura Básica 1'])
            plt.xlabel(column_name)
            plt.ylabel('Stro. Auto Cobertura Básica 1')
            plt.title(f'Scatter Plot: {column_name} vs Stro. Auto Cobertura Básica 1')
            plt.show()
        elif plot_type == '2':
            # Bar plot
            plt.bar(filtered_df[column_name], filtered_df['Stro. Auto Cobertura Básica 1'])
            plt.xlabel(column_name)
            plt.ylabel('Stro. Auto Cobertura Básica 1')
            plt.title(f'Bar Plot: {column_name} vs Stro. Auto Cobertura Básica 1')
            plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better visibility
            plt.show()
        elif plot_type == '3':
            # Line plot
            plt.plot(filtered_df[column_name], filtered_df['Stro. Auto Cobertura Básica 1'])
            plt.xlabel(column_name)
            plt.ylabel('Stro. Auto Cobertura Básica 1')
            plt.title(f'Line Plot: {column_name} vs Stro. Auto Cobertura Básica 1')
            plt.show()
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
    else:
        print(f"Column '{column_name}' not found in the DataFrame.")

if __name__ == "__main__":
    main()
