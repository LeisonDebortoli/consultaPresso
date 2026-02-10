import os
import requests

TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Identificadores do ARC Raiders
STEAM_ID = "1808500"
# ID de catálogo da Epic para ARC Raiders
EPIC_ID = "e385203309e14a8b843186259e55938d" 

def enviar_msg(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"}
    requests.post(url, data=payload)

def preco_steam():
    url = f"https://store.steampowered.com/api/appdetails?appids={STEAM_ID}&cc=br&l=portuguese"
    try:
        data = requests.get(url).json()
        if data[STEAM_ID]['success']:
            price_info = data[STEAM_ID]['data'].get('price_overview')
            if price_info:
                return price_info['final_formatted']
    except: pass
    return "Indisponível"

def preco_epic():
    url = "https://graphql.epicgames.com/graphql"
    # Query para buscar o preço regionalizado no Brasil
    query = """
    {
      Catalog {
        catalogOffers(namespace: "e385203309e14a8b843186259e55938d", params: {title: "ARC Raiders"}) {
          elements {
            price {
              totalPrice {
                fmtPrice {
                  intermediatePrice
                }
              }
            }
          }
        }
      }
    }
    """
    try:
        r = requests.post(url, json={'query': query})
        data = r.json()
        # Captura o preço formatado (Ex: R$ 171,80)
        elements = data['data']['Catalog']['catalogOffers']['elements']
        if elements:
            return elements[0]['price']['totalPrice']['fmtPrice']['intermediatePrice']
    except: pass
    return "Indisponível"

if __name__ == "__main__":
    p_steam = preco_steam()
    p_epic = preco_epic()
    
    msg = (f"🕒 *Consulta Periódica (6h)*\n\n"
           f"🎮 *ARC Raiders*\n"
           f"🔹 *Steam:* {p_steam}\n"
           f"🔹 *Epic Store:* {p_epic}\n\n"
           f"🔗 [Ver na Steam](https://store.steampowered.com/app/{STEAM_ID})\n"
           f"🔗 [Ver na Epic](https://store.epicgames.com/pt-BR/p/arc-raiders)")
    
    enviar_msg(msg)
