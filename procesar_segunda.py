import pandas as pd
import os

# Archivo de entrada
input_file = "data/raw/segunda_division_2024_25.xlsx"

# Leer Excel sin encabezados
df = pd.read_excel(input_file, header=None)

# Los nombres de los equipos visitantes están en la primera fila (columna 1 en adelante)
equipos_visitante = df.iloc[0, 1:].tolist()

# Los nombres de los equipos locales están en la primera columna (fila 1 en adelante)
equipos_local = df.iloc[1:, 0].tolist()

# Extraer la matriz de resultados (sin la primera fila ni columna)
matriz = df.iloc[1:, 1:].reset_index(drop=True)

# Crear lista de partidos
partidos = []

for i, local in enumerate(equipos_local):
    for j, visitante in enumerate(equipos_visitante):
        resultado = matriz.iat[i, j]
        
        # Ajuste para manejar diferentes tipos de guiones y nulos
        if pd.notna(resultado) and str(resultado).strip() not in ['---', '—', '--']:
            try:
                # Intentamos separar por diferentes guiones comunes
                if '–' in str(resultado):
                    goles_local, goles_visitante = map(int, str(resultado).split('–'))
                elif '-' in str(resultado):
                    goles_local, goles_visitante = map(int, str(resultado).split('-'))
                else:
                    continue
                
                partidos.append({
                    'Equipo_Local': local,
                    'Equipo_Visitante': visitante,
                    'Goles_Local': goles_local,
                    'Goles_Visitante': goles_visitante,
                    'Resultado': 1 if goles_local > goles_visitante else (-1 if goles_local < goles_visitante else 0),
                    'Competición': 'Segunda'
                })
            except Exception as e:
                # print(f"Error procesando {resultado}: {e}")
                continue

# Crear DataFrame final
df_partidos = pd.DataFrame(partidos)

# Guardar a CSV
df_partidos.to_csv("segunda_division_formateada.csv", index=False)

print("Archivo CSV generado correctamente: segunda_division_formateada.csv")
