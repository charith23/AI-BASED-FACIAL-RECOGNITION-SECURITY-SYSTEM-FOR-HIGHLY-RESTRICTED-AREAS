# core/telegram_notifier.py
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str):
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    async def send_unknown(self, image_path: str, caption: str):
        keyboard = [
            [
                InlineKeyboardButton("✅ APPROVE", callback_data="approve"),
                InlineKeyboardButton("❌ DENY", callback_data="deny"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        with open(image_path, "rb") as img:
            await self.bot.send_photo(
                chat_id=self.chat_id,
                photo=img,
                caption=caption,
                reply_markup=reply_markup
            )
