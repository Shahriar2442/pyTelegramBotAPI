import requests
from telegram import Bot
import time
from datetime import datetime

# Telegram bot info
TELEGRAM_TOKEN = '7463226295:AAHcwPUoMR1f5wXr7MbvSpwmWp9Xo1txO4I'
CHAT_ID = '-1002509018205'
bot = Bot(token=TELEGRAM_TOKEN)

# IVASMS API info
IVASMS_TOKEN = 'BZG2yDyXRap8ntPy0Ts2Deg1GNnNEAKbO6Yp1VjX'
IVASMS_ID = '228068678943115'

# Store the last OTP ID to avoid repeat
last_code = None

def fetch_otp():
    global last_code

    headers = {
        'Authorization': f'Bearer {IVASMS_TOKEN}'
    }

    url = f'https://sms.ivasms.com/api/sms/{IVASMS_ID}'

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if 'data' in data and data['data']:
            latest_sms = data['data'][0]
            sms_id = latest_sms.get('id')
            if sms_id != last_code:
                last_code = sms_id

                # Extract OTP data
                otp_message = latest_sms['body']
                otp_code = ''.join(filter(str.isdigit, otp_message))[:5]
                number = latest_sms['from']
                service = 'FACEBOOK' if 'facebook' in otp_message.lower() else 'UNKNOWN'

                # Format time
                now = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

                # Format message
                message = f"""✨ OTP Received ✨
🕰 Time: {now}
📞 Number: {number}
🛠 Service: {service}
🔑 OTP Code: {otp_code}

<#{otp_code}> is your Facebook code
H29Q Fsn4Sr"""

                # Send to Telegram
                bot.send_message(chat_id=CHAT_ID, text=message)
                print("✅ OTP sent to Telegram")

    except Exception as e:
        print(f"❌ Error fetching OTP: {e}")

# Loop every 10 seconds
while True:
    fetch_otp()
    time.sleep(10)
