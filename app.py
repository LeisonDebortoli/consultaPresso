import os
import requests

# Secrets do GitHub
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Configurações do Jogo
STEAM_ID = "1808500"
PRECO_REFERENCIA = 171.80  # O valor atual para comparação
LINK_EPIC = "https://store.epicgames.com/pt-BR/p/arc-raiders"
LINK_STEAM = f"https://store.steampowered.com/app/{STEAM_ID}"

def enviar_msg(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID, 
        "text": texto, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, data=payload)

def preco_steam():
    url = f"https://store.steampowered.com/api/appdetails?appids={STEAM_ID}&cc=br&l=portuguese"
    try:
        data = requests.get(url).json()
        if data[STEAM_ID]['success']:
            price_info = data[STEAM_ID]['data'].get('price_overview')
            if price_info:
                # Retorna o valor em centavos e a string formatada
                return price_info['final'] / 100, price_info['final_formatted']
    except:
        pass
    return None, "Indisponível"

if __name__ == "__main__":
    valor_atual, preco_texto = preco_steam()
    
    # Define o cabeçalho e o alerta baseado no preço
    if valor_atual and valor_atual < PRECO_REFERENCIA:
        header = "🚨 *ALERTA DE PROMOÇÃO!* 🚨"
        detalhe = f"📉 O preço caiu! De R$ {PRECO_REFERENCIA:.2f} por *{preco_texto}*"
    else:
        header = "🕒 *Relatório Periódico de Preço*"
        detalhe = f"💰 Preço atual na Steam: *{preco_texto}*"

    msg = (f"{header}\n\n"
           f"🎮 *ARC Raiders*\n\n"
           f"{detalhe}\n"
           f"ℹ️ _Verifique a Epic Store manualmente pelo link abaixo._\n\n"
           f"🔗 [Acessar Loja Steam]({LINK_STEAM})\n"
           f"🔗 [Acessar Loja Epic Games]({LINK_EPIC})")
    
    enviar_msg(msg)
