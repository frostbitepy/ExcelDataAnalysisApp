from preprocessing import suma_columna, eliminar_nulls



def procesar_siniestros(siniestros_df):
    # Eliminar filas que no son sinietros teniendo en cuenta
    # los valores nulos en la columna 'Fec. Stro.'
    df = eliminar_nulls(siniestros_df, 'Fec. Stro.')
    
    return df


def sumar_siniestros(siniestros_df):
    # Sumar los sinietros
    return suma_columna(siniestros_df, 'Auto Cober. Básica 1')


def cantidad_siniestros(siniestros_df):
    # Sumar las filas del dataframe
    return len(siniestros_df)