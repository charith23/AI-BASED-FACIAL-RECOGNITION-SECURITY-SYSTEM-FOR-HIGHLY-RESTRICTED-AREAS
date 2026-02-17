import os
import requests

TOKEN = os.getenv("TG_BOT_TOKEN")
url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
print(requests.get(url).text)
