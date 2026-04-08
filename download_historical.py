import urllib.request
import os

# Directorio de destino
dest_dir = "data/historical"
os.makedirs(dest_dir, exist_ok=True)

# URL base y temporadas
base_url = "https://www.football-data.co.uk/mmz4281"
seasons = ["2425", "2324", "2223", "2122", "2021", "1920"]
leagues = ["SP1", "SP2"]

print("Iniciando descarga de datos históricos...")

for season in seasons:
    for league in leagues:
        url = f"{base_url}/{season}/{league}.csv"
        filename = f"{dest_dir}/{league}_{season}.csv"
        
        try:
            print(f"Descargando {league} Temporada {season}...")
            urllib.request.urlretrieve(url, filename)
        except Exception as e:
            print(f"Error descargando {url}: {e}")

print("\nDescarga completada en data/historical/")
