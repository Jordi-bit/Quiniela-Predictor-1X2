import pandas as pd

# Cargar archivo xlsx
input_file = "data/raw/la-liga-2024-UTC.xlsx"
df = pd.read_excel(input_file)

# Convertir fecha a formato YYYY-MM-DD
df['Fecha'] = pd.to_datetime(df['Fecha']).dt.strftime('%Y-%m-%d')

# Separar goles
# Suponemos que Resultado está en formato "1 - 1"
# El archivo tiene espacios entre el guion, así que strip() es importante
df[['Goles_Local','Goles_Visitante']] = df['Resultado'].str.split('-', expand=True)

df['Goles_Local'] = df['Goles_Local'].str.strip().astype(int)
df['Goles_Visitante'] = df['Goles_Visitante'].str.strip().astype(int)

# Calcular Resultado 1X2
def resultado_1x2(row):
    if row['Goles_Local'] > row['Goles_Visitante']:
        return 1
    elif row['Goles_Local'] < row['Goles_Visitante']:
        return -1
    else:
        return 0

df['Resultado'] = df.apply(resultado_1x2, axis=1)

# Agregar columna Competición
df['Competición'] = 'Primera'

# Seleccionar columnas finales
df_final = df[['Fecha','Equipo_Local','Equipo_Visitante','Goles_Local','Goles_Visitante','Resultado','Competición']]

# Guardar a CSV
df_final.to_csv("primera_division_formateada.csv", index=False)

print("Archivo CSV generado: primera_division_formateada.csv")
