import requests

# Telegram Bot API Info
TELEGRAM_BOT_TOKEN = "7520926677:AAHEkX-QJ6yBaP57lgWzgonNAdSN1Z209qQ"
TELEGRAM_CHAT_ID = "-1002386406118"  # Group ID
MESSAGE_THREAD_ID = 2  # Topic ID (Notification Thread)

def send_telegram_alert(someone, message_text):
    """Send a Telegram alert to the 'Notification' topic in the supergroup."""
    
    message = f"🚨 ALERT: {someone} fell!\n📩 Message: {message_text}"
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "message_thread_id": MESSAGE_THREAD_ID,  # Ensures message goes to the "Notification" topic
        "text": message
    }
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        print("📢 Telegram alert sent to Notification topic!")
    else:
        print(f"❌ Failed to send alert. Error: {response.json()}")

# Test Function
send_telegram_alert("John Doe", "I need help, I just fell!")
