import requests
import cv2

BOT_TOKEN = "8296389928:AAHX3dhadGpBpldT61CgDLdcIrmPam1OFn8"
CHAT_ID = "-5128242687"
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_alert(frame):
    try:
        _, img = cv2.imencode(".jpg", frame)
        files = {"photo": img.tobytes()}

        requests.post(
            f"{API}/sendPhoto",
            data={
                "chat_id": CHAT_ID,
                "caption": "⚠️ UNKNOWN FACE DETECTED"
            },
            files=files,
            timeout=5
        )
        print("[ALERT] Telegram sent")

    except Exception as e:
        print("[WARN] Telegram failed:", e)
