import os
import requests

# O GitHub Actions injeta os Secrets aqui
TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

# Dados do ARC Raiders
GAME_STEAM_ID = "1808500" 
PRECO_ALVO_CENTAVOS = 17180  # Referência do preço atual R$ 171,80

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
                
                # Lógica de comparação para o ícone
                if preco_final < PRECO_ALVO_CENTAVOS:
                    status = "📉 *PROMOÇÃO DETECTADA!*"
                else:
                    status = "ℹ️ *Relatório Diário de Preço*"

                msg = (f"{status}\n\n"
                       f"🎮 *Jogo:* {titulo}\n"
                       f"💰 *Preço Atual:* {preco_formatado}\n"
                       f"🔗 [Ver na Steam](https://store.steampowered.com/app/{GAME_STEAM_ID})")
                
                enviar_mensagem(msg)
                print(f"Mensagem enviada: {titulo} - {preco_formatado}")
            else:
                enviar_mensagem(f"⚠️ *Aviso:* O jogo ARC Raiders está sem preço visível na API da Steam no momento.")
        else:
            print("Falha ao consultar a API da Steam.")
            
    except Exception as e:
        print(f"Erro na execução: {e}")

if __name__ == "__main__":
    if not TOKEN or not CHAT_ID:
        print("Erro: Variáveis de ambiente TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não encontradas.")
    else:
        verificar_preco()
