import webview
import os
import sys

def resource_path(relative_path):
    """
    Obtiene la ruta absoluta al recurso, funciona dentro del .exe creado con PyInstaller.
    """
    try:
        # Ruta temporal creada por PyInstaller
        base_path = sys._MEIPASS
    except AttributeError:
        # Ejecutando desde Python
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def main():
    # Construir ruta absoluta a index.html dentro del bundle
    ruta_html = resource_path("index.html")
    
    # Crear la ventana
    window = webview.create_window(
        "⚽ Predicción Quiniela 1X2",
        f"file:///{ruta_html}",
        width=600,
        height=700,
        resizable=True
    )
    
    # Iniciar el webview
    # Nota: En desarrollo, puedes activar gui='edgehtml' o 'cef' si tienes problemas
    webview.start()

if __name__ == "__main__":
    main()
