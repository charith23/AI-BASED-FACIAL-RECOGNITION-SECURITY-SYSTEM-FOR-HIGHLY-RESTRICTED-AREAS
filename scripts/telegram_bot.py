import telebot
import threading
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class TelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token, parse_mode="HTML")
        self.last_sent = 0
        self.cooldown = 10  # seconds

    def send_unknown_alert(self, chat_id, image_path=None):
        now = time.time()
        if now - self.last_sent < self.cooldown:
            return  # STOP SPAM

        self.last_sent = now

        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton("✅ Approve", callback_data="approve"),
            InlineKeyboardButton("❌ Deny", callback_data="deny")
        )
        markup.row(
            InlineKeyboardButton("➕ Add as New", callback_data="add_new")
        )

        def _send():
            try:
                if image_path:
                    with open(image_path, "rb") as img:
                        self.bot.send_photo(
                            chat_id=chat_id,
                            photo=img,
                            caption="🚨 <b>Unknown Face Detected</b>",
                            reply_markup=markup,
                            timeout=10
                        )
                else:
                    self.bot.send_message(
                        chat_id,
                        "🚨 <b>Unknown Face Detected</b>",
                        reply_markup=markup
                    )
            except Exception as e:
                print("[TELEGRAM ERROR]", e)

        threading.Thread(target=_send, daemon=True).start()
