import pandas as pd
import json
import os

# Cargar el dataset unificado de 5 años
try:
    df = pd.read_csv("historico_5_anos.csv")

    # Convertir a una lista de diccionarios para el JSON
    # Incluimos el Peso por si la web quiere usarlo en el futuro
    columnas_necesarias = ['Equipo_Local', 'Equipo_Visitante', 'Goles_Local', 'Goles_Visitante', 'Resultado']
    
    # Manejar columnas faltantes si es necesario
    df_filtrado = df[[col for col in columnas_necesarias if col in df.columns]]
    historial = df_filtrado.to_dict(orient='records')

    # También añadimos una lista de equipos "actuales" (temporada 2425) para los dropdowns
    # (Esto lo podríamos hacer aquí o en el JS, pero aquí es más eficiente)
    # Leemos los CSVs actuales para identificar qué equipos juegan hoy
    if 'Peso' in df.columns:
        equipos_actuales = sorted(list(set(df[df['Peso'] == 1.0]['Equipo_Local'].unique())))
    else:
        equipos_actuales = sorted(list(set(df['Equipo_Local'].unique())))

    data_final = {
        "partidos": historial,
        "equipos_actuales": equipos_actuales
    }

    with open('historial.json', 'w', encoding='utf-8') as f:
        json.dump(data_final, f, ensure_ascii=False, indent=4)

    print(f"✅ historial.json generado con {len(historial)} partidos y {len(equipos_actuales)} equipos actuales.")
except FileNotFoundError:
    print("Error: Asegúrate de ejecutar primero unir_datasets.py")
