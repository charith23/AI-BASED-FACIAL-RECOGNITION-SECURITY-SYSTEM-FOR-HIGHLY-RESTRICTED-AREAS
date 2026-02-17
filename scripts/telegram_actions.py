class TelegramActions:
    def __init__(self, bot):
        self.bot = bot

    def handle_callback(self, call):
        data = call.data
        chat_id = call.message.chat.id

        if data == "approve":
            self.bot.send_message(chat_id, "✅ Access approved")

        elif data == "deny":
            self.bot.send_message(chat_id, "❌ Access denied")

        elif data == "add_face":
            self.bot.send_message(chat_id, "✍️ Send person name")

        elif data == "one_time":
            self.bot.send_message(chat_id, "🚫 One‑time access granted")
