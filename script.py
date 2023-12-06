import pandas as pd
import numpy as np

file = "LSITADO_generado-prod.csv"

# Read a csv file and convert to xlsx file
def csv_to_xlsx(csv_file_path, xlsx_file_path):
    read_file = pd.read_csv(csv_file_path)
    read_file.to_excel(xlsx_file_path, index=None, header=True)
    return read_file

# Read an excel file
def read_excel(file_path):
    df = pd.read_excel(file_path)
    return df



# Convert the file
csv_to_xlsx(file, "Listado_generado.xlsx")



