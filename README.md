# ⚽ Quiniela Predictor 1X2

Este proyecto utiliza Machine Learning para predecir los resultados de los partidos de la Quiniela (1X2) de las ligas españolas de fútbol (Primera y Segunda División). Utiliza un modelo de red neuronal entrenado con datos históricos de la temporada 2024-2025.

## 🚀 Características
- **Procesamiento de Datos**: Scripts en Python para limpiar y unificar datos desde archivos Excel.
- **Entrenamiento Robusto**: Generación manual de un modelo TensorFlow.js compatible sin dependencias complejas de Python.
- **Interfaz Web Moderna**: Interfaz en **Modo Oscuro** con alta legibilidad y rapidez de respuesta.
- **Predicción Inteligente**: Basada en promedios de goles, rachas de victorias y ventaja de campo.

## 📂 Estructura del Proyecto
- `app.js`: Lógica de predicción en el navegador usando TensorFlow.js.
- `index.html`: Interfaz de usuario (HTML/CSS).
- `train_model.py`: Script de entrenamiento de la red neuronal y exportación al formato web.
- `procesar_*.py`: Scripts para normalizar los datos de entrada.
- `data/raw/`: Carpeta que contiene los datos originales en formato Excel.
- `web_model/`: Contiene el modelo entrenado (JSON y pesos binarios).
- `historial.json`: Datos procesados para uso rápido en la interfaz.

## 🛠️ Instalación y Uso

### 1. Preparar el entorno
Asegúrate de tener Python instalado y las dependencias necesarias:
```bash
pip install -r requirements.txt
```

### 2. Generar el modelo
Si añades nuevos datos en la carpeta `data/raw/`, puedes reentrenar el modelo ejecutando:
```bash
python procesar_primera.py
python procesar_segunda.py
python unir_datasets.py
python generar_historial.py
python train_model.py
```

### 3. Ejecutar la aplicación
Debido a las políticas de seguridad de los navegadores (CORS), no puedes abrir el archivo `index.html` directamente. Debes usar un servidor local:
```bash
python -m http.server 8000
```
Luego visita `http://localhost:8000` en tu navegador.

## 📄 Licencia
Este proyecto está bajo la Licencia MIT.

---
Desarrollado para predicción avanzada de resultados deportivos.
