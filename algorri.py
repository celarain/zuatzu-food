import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime
import re
from utils import enviar_mensaje_google_chat, format_data_as_markdown

def get_menu():
    response = requests.get("https://algorrijatetxea.com/menus/7-algorri-en-la-oficina/")
    html = BeautifulSoup(response.content, "html.parser")
    platos = {}
    current_bloque = None

    for plato_tag in html.find_all("div", class_="list-group-item"):
        for tag in plato_tag.find_all(["span"]):
            text = tag.get_text().strip().upper()
            if tag.find_all(["strong"]) and 'font-size: 18.6667px;' in tag.get('style') and text not in 'MENÚ ALGORRI EN LA OFICINA:':
                current_bloque = text
                if current_bloque not in platos:
                    platos[current_bloque] = []
                    continue
            else:
                if current_bloque is not None and '€' not in text and '$' not in text:
                    platos[current_bloque].append(text)
    return platos

if __name__ == "__main__":
    print("Empiezo Algorri")
    menu_data = format_data_as_markdown(get_menu())
    menu_data = str(menu_data)
    menu = "```ALGORRI JATETXEA " + datetime.now().strftime('%d/%m/%Y') + " - 943 21 82 79```\n" + menu_data + "\n\n"
    #enviar_mensaje_google_chat(menu, "algorri")
    print("Acabo Algorri")