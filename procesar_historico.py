import pandas as pd
import os
import json

# Directorios
hist_dir = "data/historical"
output_file = "historico_5_anos.csv"

# Mapeo de nombres (Historical -> Standard)
# Intentamos normalizar a los nombres que usa el historial.json actual
mapping = {
    "Alaves": "Deportivo Alavés",
    "Ath Bilbao": "Athletic Club",
    "Ath Madrid": "Atlético de Madrid",
    "Barcelona": "FC Barcelona",
    "Celta": "RC Celta",
    "Espanol": "RCD Espanyol de Barcelona",
    "Getafe": "Getafe CF",
    "Girona": "Girona FC",
    "Las Palmas": "UD Las Palmas",
    "Leganes": "CD Leganés",
    "Mallorca": "RCD Mallorca",
    "Osasuna": "CA Osasuna",
    "Sociedad": "Real Sociedad",
    "Sevilla": "Sevilla FC",
    "Valencia": "Valencia CF",
    "Valladolid": "Real Valladolid CF",
    "Vallecano": "Rayo Vallecano",
    "Villarreal": "Villarreal CF",
    "Sp Gijon": "SPORTING",
    "Santander": "RACING",
    "La Coruna": "DEPORTIVO",
    # Equipos de Segunda que suelen venir en mayúsculas en el Excel del usuario
    "Albacete": "ALBACETE",
    "Almeria": "ALMERIA",
    "Burgos": "BURGOS",
    "Cadiz": "CADIZ",
    "Cartagena": "CARTAGENA",
    "Castellon": "CASTELLON",
    "Cordoba": "CORDOBA",
    "Eibar": "EIBAR",
    "Elche": "ELCHE",
    "Eldense": "ELDENSE",
    "Ferrol": "FERROL",
    "Granada": "GRANADA",
    "Huesca": "HUESCA",
    "Levante": "LEVANTE",
    "Malaga": "MALAGA",
    "Mirandes": "MIRANDES",
    "Oviedo": "OVIEDO",
    "Tenerife": "TENERIFE",
    "Zaragoza": "ZARAGOZA",
}

# Pesos por temporada
weights = {
    "2425": 1.0,
    "2324": 0.8,
    "2223": 0.6,
    "2122": 0.4,
    "2021": 0.2,
    "1920": 0.1
}

all_data = []

print("Procesando archivos históricos...")
for f in os.listdir(hist_dir):
    if f.endswith(".csv"):
        # Extraer temporada del nombre del archivo (ej: SP1_2324.csv)
        season = f.split("_")[1].replace(".csv", "")
        weight = weights.get(season, 0.1)
        
        try:
            df = pd.read_csv(os.path.join(hist_dir, f), encoding='latin1')
            
            # Seleccionar columnas necesarias
            # Football-data usa: HomeTeam, AwayTeam, FTHG, FTAG, FTR
            df_subset = df[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']].copy()
            
            # Aplicar mapeo
            df_subset['Equipo_Local'] = df_subset['HomeTeam'].map(lambda x: mapping.get(x, x))
            df_subset['Equipo_Visitante'] = df_subset['AwayTeam'].map(lambda x: mapping.get(x, x))
            
            # Convertir resultado a nuestro formato (1: Local, 0: Empate, -1: Visitante)
            def map_res(r):
                if r == 'H': return 1
                if r == 'A': return -1
                return 0
            
            df_subset['Resultado'] = df_subset['FTR'].apply(map_res)
            df_subset['Peso'] = weight
            df_subset['Goles_Local'] = df_subset['FTHG']
            df_subset['Goles_Visitante'] = df_subset['FTAG']
            
            all_data.append(df_subset[['Equipo_Local', 'Equipo_Visitante', 'Goles_Local', 'Goles_Visitante', 'Resultado', 'Peso']])
        except Exception as e:
            print(f"Error procesando {f}: {e}")

# Unificar todo
df_final = pd.concat(all_data, ignore_index=True)
df_final.to_csv(output_file, index=False)
print(f"✅ Histórico unificado generado: {output_file} ({len(df_final)} partidos)")
