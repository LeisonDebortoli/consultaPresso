import os
import requests

# O GitHub Actions injeta os Secrets aqui
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Dados do ARC Raiders
GAME_STEAM_ID = "1808500" 
PRECO_ALVO_CENTAVOS = 17180  # R$ 171,80 em centavos

def enviar_mensagem(texto):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto, "parse_mode": "Markdown"}
    try:
        r = requests.post(url, data=payload)
        r.raise_for_status()
    except Exception as e:
        print(f"Erro ao enviar para o Telegram: {e}")

def verificar_preco():
    # API Oficial da Steam (cc=br para Reais)
    url = f"https://store.steampowered.com/api/appdetails?appids={GAME_STEAM_ID}&cc=br&l=portuguese"
    
    try:
        response = requests.get(url).json()
        
        if response and response[GAME_STEAM_ID]['success']:
            data = response[GAME_STEAM_ID]['data']
            
            if 'price_overview' in data:
                preco_final = data['price_overview']['final']
                preco_formatado = data['price_overview']['final_formatted']
                titulo = data['name']
                
                print(f"Relatório 12h: {titulo} está custando {preco_formatado}")

                # Verifica se houve queda de preço
                if preco_final < PRECO_ALVO_CENTAVOS:
                    msg = (f"📉 *PROMOÇÃO DETECTADA!*\n\n"
                           f"🎮 *Jogo:* {titulo}\n"
                           f"💰 *Preço:* {preco_formatado}\n"
                           f"🔗 [Ver na Steam](https://store.steampowered.com/app/{GAME_STEAM_ID})")
                    enviar_mensagem(msg)
                else:
                    # Opcional: Avisar que o preço continua o mesmo (para você saber que o bot rodou)
                    # enviar_mensagem(f"ℹ️ Check diário: {titulo} continua {preco_formatado}.")
                    pass
            else:
                print("Jogo sem informações de preço no momento.")
        else:
            print("Falha ao consultar a API da Steam.")
            
    except Exception as e:
        print(f"Erro na execução: {e}")

if __name__ == "__main__":
    if not TOKEN or not CHAT_ID:
        print("Erro: Variáveis de ambiente TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não encontradas.")
    else:
        verificar_preco()
