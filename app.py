import os
import requests
import time
from datetime import datetime

# Configurações fornecidas
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GAME_STEAM_ID = "1808500" 
PRECO_ALVO_CENTAVOS = 17180 

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto}
    requests.post(url, data=payload)

def verificar_preco_steam():
    url = f"https://store.steampowered.com/api/appdetails?appids={GAME_STEAM_ID}&cc=br&l=portuguese"
    try:
        response = requests.get(url).json()
        if response and response[GAME_STEAM_ID]['success']:
            data = response[GAME_STEAM_ID]['data']
            if 'price_overview' in data:
                preco_final = data['price_overview']['final']
                preco_formatado = data['price_overview']['final_formatted']
                
                if preco_final < PRECO_ALVO_CENTAVOS:
                    enviar_mensagem(f"📉 PROMOÇÃO: ARC Raiders por {preco_formatado}!")
                    return True
                else:
                    print(f"Check 12h: Preço ainda em {preco_formatado}")
    except Exception as e:
        print(f"Erro: {e}")
    return False

print("Monitor agendado para as 12:00h iniciado...")

while True:
    agora = datetime.now()
    # Verifica se é 12:00 (ajuste para o fuso horário do servidor se necessário)
    if agora.hour == 12 and agora.minute == 0:
        verificar_preco_steam()
        time.sleep(70) # Espera 70s para não executar duas vezes no mesmo minuto
    
    time.sleep(30) # Checa o relógio a cada 30 segundos
