import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
from utils import enviar_mensaje_google_chat, format_data_as_markdown

def get_menu():
    response = requests.get("https://www.inausti.net/")
    html = BeautifulSoup(response.content, "html.parser")
    platos = {}
    current_bloque = None

    for plato_tag in html.find_all("div", attrs={"data-id": "paoc-popup-4126"}):
        for tag in plato_tag.find_all(["em"]):
            text = tag.get_text().strip().upper()
            if tag.find_all(["strong"]):
                current_bloque = text
                if current_bloque not in platos:
                    platos[current_bloque] = []
                    continue
            else:
                if current_bloque is not None:
                    platos[current_bloque].append(text)
    return platos

if __name__ == "__main__":
    print("Empiezo inausti")
    menu_data = format_data_as_markdown(get_menu())
    menu_data = str(menu_data)
    menu = "```RESTAURANTE IÑAUSTI " + datetime.now().strftime('%d/%m/%Y') + " - 943 31 39 33```\n" + menu_data + "\n\n"
    enviar_mensaje_google_chat(menu, "inausti")
    print("Fin inausti")