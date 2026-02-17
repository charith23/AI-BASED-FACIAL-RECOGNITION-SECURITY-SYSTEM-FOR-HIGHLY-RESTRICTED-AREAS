# core/bot_handler.py
import telebot
import logging
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import threading
import time

telebot.logger.setLevel(logging.WARNING)

class BotHandler:
    def __init__(self, token, allowed_chat_id):
        self.bot = telebot.TeleBot(token)
        self.chat_id = allowed_chat_id
        self.command_queue = [] 
        
        self.thread = threading.Thread(target=self.start_polling, daemon=True)
        self.thread.start()

    def start_polling(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_query(call):
            if str(call.message.chat.id) != self.chat_id: return

            if call.data == "ask_action":
                markup = InlineKeyboardMarkup()
                markup.row(InlineKeyboardButton("🚪 OPEN DOOR", callback_data="one_time"))
                markup.row(InlineKeyboardButton("👤 ADD FACE", callback_data="add_face_init"))
                try:
                    self.bot.edit_message_caption(chat_id=self.chat_id, message_id=call.message.message_id, 
                                                caption="✅ **Accepted.** Choose Action:", reply_markup=markup)
                except: pass

            elif call.data == "deny":
                self.bot.answer_callback_query(call.id, "🚫 Denied")
                try:
                    self.bot.edit_message_caption(chat_id=self.chat_id, message_id=call.message.message_id, caption="🚫 **DENIED.**")
                except: pass
                self.command_queue.append(("DENY", None))

            elif call.data == "one_time":
                self.bot.answer_callback_query(call.id, "🚪 Opening...")
                self.bot.send_message(self.chat_id, "🔓 **Access Granted.**")
                self.command_queue.append(("OPEN", None))

            elif call.data == "add_face_init":
                self.bot.answer_callback_query(call.id, "Type Name...")
                msg = self.bot.send_message(self.chat_id, "✍️ **Enter Name for New Person:**")
                self.bot.register_next_step_handler(msg, self.get_name_step)

        while True:
            try:
                self.bot.infinity_polling(timeout=20, long_polling_timeout=10)
            except Exception as e:
                time.sleep(5)

    def get_name_step(self, message):
        name = message.text.strip()
        if name:
            self.bot.send_message(self.chat_id, f"📸 Capturing photos for {name}...\nMove your head SLOWLY!")
            self.command_queue.append(("TRAIN", name))

    def send_alert(self, frame_bytes):
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("✅ ACCEPT", callback_data="ask_action")
        btn2 = InlineKeyboardButton("❌ DENY", callback_data="deny")
        markup.add(btn1, btn2)

        try:
            self.bot.send_photo(self.chat_id, frame_bytes, caption="⚠️ **UNKNOWN FACE DETECTED!**", reply_markup=markup)
            return True
        except Exception as e:
            print(f"[BOT ERROR] Send Failed: {e}")
            return False

    def get_command(self):
        if self.command_queue: return self.command_queue.pop(0)
        return None