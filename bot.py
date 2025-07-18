import requests
import time
from telegram import Bot
from datetime import datetime

# Bot Config
BOT_TOKEN = '7463226295:AAHcwPUoMR1f5wXr7MbvSpwmWp9Xo1txO4I'
CHAT_ID = '-1002509018205'

# IVASMS Config
IVASMS_ID = '228068678943115'
IVASMS_TOKEN = 'BZG2yDyXRap8ntPy0Ts2Deg1GNnNEAKbO6Yp1VjX'

# Initialize Bot
bot = Bot(token=BOT_TOKEN)

# Store last message ID to avoid duplicates
last_message_id = None

def get_otp_from_ivasms():
    url = f"https://ivasms.com/api/messages/{IVASMS_ID}?token={IVASMS_TOKEN}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            messages = response.json()
            if not messages:
                return None
            return messages[0]  # latest message
        else:
            print("Error fetching IVASMS:", response.status_code)
            return None
    except Exception as e:
        print("Exception:", e)
        return None

def send_to_telegram(msg):
    otp_code = msg['message'].split()[0]
    number = msg['sender']
    time_obj = datetime.strptime(msg['date'], "%Y-%m-%d %H:%M:%S")
    timestamp = time_obj.strftime("%d/%m/%Y, %H:%M:%S")

    full_msg = (
        "✨ OTP Received ✨\n"
        f"⏰ Time: {timestamp}\n"
        f"📞 Number: {number}\n"
        f"🛠️ Service: FACEBOOK\n"
        f"🔑 OTP Code: {otp_code}\n\n"
        f"```{msg['message']}```"
    )

    bot.send_message(chat_id=CHAT_ID, text=full_msg, parse_mode='Markdown')

def main():
    global last_message_id
    while True:
        msg = get_otp_from_ivasms()
        if msg and msg['id'] != last_message_id:
            send_to_telegram(msg)
            last_message_id = msg['id']
        time.sleep(5)

if __name__ == "__main__":
    main()
