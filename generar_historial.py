import pandas as pd
import json

# Cargar CSV
try:
    df = pd.read_csv("todas_divisiones_2024_2025.csv")

    # Seleccionar solo las columnas necesarias
    df = df[['Equipo_Local', 'Equipo_Visitante', 'Goles_Local', 'Goles_Visitante', 'Resultado']]

    # Convertir a lista de diccionarios
    historial_list = df.to_dict(orient='records')

    # Guardar como JSON
    with open('historial.json', 'w', encoding='utf-8') as f:
        json.dump(historial_list, f, ensure_ascii=False, indent=4)

    print("Archivo historial.json generado correctamente")
except FileNotFoundError:
    print("Error: Asegúrate de ejecutar primero unir_datasets.py")
