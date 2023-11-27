import requests
import json
from datetime import datetime
import os

def enviar_mensaje_google_chat(mensaje, restaurant):
    #Vamos a comprobar si el texto que vamos a enviar es igual al último que enviamos
    #para evitar enviar mensajes duplicados
    is_equal = compare_last_menu(restaurant, mensaje)
    if not is_equal:
        #guardamos el menú en un log
        save_menu_in_log(restaurant, mensaje)
        PROD_MODE = get_boolean_from_string(os.environ.get("PROD_MODE", False))
        if PROD_MODE:
            WEBHOOK_URL = os.environ.get("WEBHOOK_URL_PROD")
        else:
            WEBHOOK_URL =  os.environ.get("WEBHOOK_URL_DEV")

        payload = {"text": mensaje}
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        response = requests.post(WEBHOOK_URL, data=json.dumps(payload), headers=headers)

        if response.status_code == 200:
            print("Mensaje enviado con éxito a Google Chat")
        else:
            print(f"Error al enviar el mensaje: {response.status_code} - {response.text}")
    else:
        print("El mensaje es igual al último que enviamos, no lo enviamos")

def format_data_as_markdown(data):
    markdown = ""
    for category, dishes in data.items():
        markdown += f"\n`{category}`\n\n"
        for dish in dishes:
            markdown += f"      - {dish}\n"
    return markdown

def get_boolean_from_string(key):
    boolean_result = str(key).lower() in ("true", "1", "yes", "y")
    return boolean_result

def save_menu_in_log(restaurant, text):
    print("Guardando el menú en un log")
    with open(f"logs/{restaurant}.log", "w") as f:
        f.write(text)

def compare_last_menu(restaurant, text):
    # Tomar sólo el texto después del primer salto de línea
    file_path = f"logs/{restaurant}.log"
    if not os.path.exists(file_path):
        return False  # o cualquier valor predeterminado que quieras devolver si el archivo no existe

    cleaned_text = "\n".join(text.split("\n")[1:])

    with open(f"logs/{restaurant}.log", "r") as f:
        last_menu = f.read()
        # Omitir la primera línea del último menú registrado
        cleaned_last_menu = "\n".join(last_menu.split("\n")[1:])

        return cleaned_text == cleaned_last_menu

