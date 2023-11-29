def devengado(V5, W5, AA1, AA2):
    if W5 < AA1 or V5 > AA2:
        return 0
    elif V5 <= AA1 and W5 <= AA2:
        return W5 - AA1
    elif V5 > AA1 and W5 <= AA2:
        return W5 - V5
    elif V5 > AA1 and W5 > AA2:
        return AA2 - V5
    elif V5 < AA1 and W5 > AA2:
        return AA2 - AA1
    else:
        return None  # Manejar cualquier otro caso según sea necesario

# Ejemplo de uso:
V5_valor = 10  # Reemplazar con el valor real de V5
W5_valor = 15  # Reemplazar con el valor real de W5
AA1_valor = 5  # Reemplazar con el valor real de AA1
AA2_valor = 20  # Reemplazar con el valor real de AA2

resultado = devengado(V5_valor, W5_valor, AA1_valor, AA2_valor)
print(resultado)


def rrc_unidad(y_valor, z_valor):
    if y_valor > 0:
        return z_valor / y_valor
    else:
        return None  # Otra opción podría ser devolver un valor predeterminado en lugar de None

# Ejemplo de uso:
y_valor = 5  # Reemplazar con el valor real de Y5
z_valor = 20  # Reemplazar con el valor real de Z5

resultado = rrc_unidad(y_valor, z_valor)
print(resultado)


def reserva_de_riesgo_en_curso(y_valor, aa_valor, x_valor):
    if y_valor > 0:
        return aa_valor * x_valor
    else:
        return None  # Puedes ajustar esto para devolver un valor predeterminado si lo prefieres

# Ejemplo de uso:
y_valor = 5  # Reemplazar con el valor real de Y6
aa_valor = 10  # Reemplazar con el valor real de AA6
x_valor = 3  # Reemplazar con el valor real de X6

resultado = reserva_de_riesgo_en_curso(y_valor, aa_valor, x_valor)
print(resultado)


from datetime import datetime, timedelta

def mi_funcion_devengamiento(fecha_desde, fecha_hasta, inicio_corte, fin_corte):
    fecha_desde = datetime.strptime(fecha_desde, "%Y-%m-%d")
    fecha_hasta = datetime.strptime(fecha_hasta, "%Y-%m-%d")
    inicio_corte = datetime.strptime(inicio_corte, "%Y-%m-%d")
    fin_corte = datetime.strptime(fin_corte, "%Y-%m-%d")

    if fecha_hasta < inicio_corte or fecha_desde > fin_corte:
        return 0
    elif fecha_desde <= inicio_corte and fecha_hasta <= fin_corte:
        return (fecha_hasta - inicio_corte).days
    elif fecha_desde > inicio_corte and fecha_hasta <= fin_corte:
        return (fecha_hasta - fecha_desde).days
    elif fecha_desde > inicio_corte and fecha_hasta > fin_corte:
        return (fin_corte - fecha_desde).days
    elif fecha_desde < inicio_corte and fecha_hasta > fin_corte:
        return (fin_corte - inicio_corte).days

# Ejemplo de uso
fecha_desde = "2023-01-01"
fecha_hasta = "2023-06-30"
inicio_corte = "2023-03-01"
fin_corte = "2023-09-01"

resultado = mi_funcion_devengamiento(fecha_desde, fecha_hasta, inicio_corte, fin_corte)
print(resultado)