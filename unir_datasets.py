import pandas as pd

# Cargar los CSV
try:
    primera = pd.read_csv("primera_division_formateada.csv")
    segunda = pd.read_csv("segunda_division_formateada.csv")

    # Unir ambos datasets
    todos_partidos = pd.concat([primera, segunda], ignore_index=True)

    # Guardar en un nuevo CSV
    todos_partidos.to_csv("todas_divisiones_2024_2025.csv", index=False)

    print("CSV combinado generado: todas_divisiones_2024_2025.csv")
except FileNotFoundError:
    print("Error: Asegúrate de ejecutar primero procesar_primera.py y procesar_segunda.py")
