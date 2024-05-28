from preprocessing import suma_columna, eliminar_nulls



def procesar_siniestros(siniestros_df):
    # Eliminar filas que no son sinietros teniendo en cuenta
    # los valores nulos en la columna 'Fec. Stro.'
    df = eliminar_nulls(siniestros_df, 'Fec. Stro.')
    
    return df


def deprecated_sumar_siniestros(siniestros_df):
    # Sumar los sinietros
    return suma_columna(siniestros_df, 'Auto Cober. Básica 1')


# Suma todas las columnas de siniestros de las operaciones y returna un valor
def sumar_siniestros(siniestros_df):
    # List of columns to sum
    columns_to_sum = ['Stro. Auto Cobertura Básica 1', 'Stro. Auto Cobertura Básica 2', 'Stro. Auto Lesión Una Per. Art.', 'Stro. Auto Lesión 2 o más Per. Art.', 'Stro. Auto Robo Veh. Art.', 'Stro. Auto Accesorios Art.', 'Stro. Auto Daños Material a Ter. Art.', 'Stro. Auto Muerte/Incap. Art.', 'Stro. Auto Asist. Médica Art.', 'Stro. Auto Otras Coberturas Art.']

    # Sum the values of the specified columns
    total_sum = siniestros_df[columns_to_sum].sum().sum()

    return total_sum


def cantidad_siniestros(siniestros_df):
    # Sumar las filas del dataframe
    return len(siniestros_df)