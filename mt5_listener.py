import MetaTrader5 as mt5
import time
import urllib.request
import json

# ⚠️ BUL JERGE BOTFATHER BERGEN API KILTIN QOYASYZ
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
# ⚠️ BUL JERGE TELEGRAM KANALIŃIZDYN USERNAME-IN JAZASYZ (Mısalı: "@my_channel_name")
CHANNEL_ID = "@YOUR_CHANNEL_USERNAME" 

print("MT5 Tıńshı Robotı internet rejiminde iske tústi...")
if not mt5.initialize():
    print("MetaTrader5 qátelik, robot toqtatıldı.")
    quit()

history_deals = mt5.history_deals_get(time.time() - 86400 * 3, time.time() + 86400)
last_checked_ticket = max(deal.ticket for deal in history_deals) if history_deals else 0

def send_to_telegram(trade_data):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        # Sayt tapsırıp alıwı ańsat bolıwı úshin text formatında json jiberemiz
        text_message = json.dumps(trade_data)
        
        payload = {
            "chat_id": CHANNEL_ID,
            "text": text_message
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req) as response:
            pass
        print(f"[INTERNET] Sawda Telegram kanalǵa dynamic ketti!")
    except Exception as e:
        print("Telegramǵa jiberiwde kedergi:", e)

while True:
    try:
        curr_account = mt5.account_info()
        history_deals = mt5.history_deals_get(time.time() - 86400 * 3, time.time() + 86400)
        
        if history_deals:
            for deal in history_deals:
                if deal.ticket > last_checked_ticket and deal.entry == 1:
                    last_checked_ticket = deal.ticket
                    
                    duration_min = int((deal.time - deal.time_msc/1000) / 60)
                    if duration_min < 0: duration_min = 0
                    
                    trade_info = {
                        "accountLogin": int(curr_account.login),
                        "brokerName": str(curr_account.company),
                        "ticket": int(deal.ticket),
                        "symbol": str(deal.symbol),
                        "profit": float(deal.profit),
                        "direction": "UZUN" if deal.type == 0 else "QISQA",
                        "duration": duration_min,
                        "closeTime": int(deal.time) * 1000
                    }
                    
                    send_to_telegram(trade_info)
                        
    except Exception as e:
        print("Sistemada qátelik:", e)
        
    time.sleep(2)