# inline keyboard
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

DICTIONARY_KEY = "dictionary"
LANGUAGE_KEY = "language"
BACK_KEY = "back"

main_keyboard = [
    [
        InlineKeyboardButton("📝 Dictionary",
                             callback_data=DICTIONARY_KEY),
    ],
    [InlineKeyboardButton("🌍 Language", callback_data=LANGUAGE_KEY),],
    [InlineKeyboardButton("🔙 Back", callback_data=BACK_KEY)],
]

main_keyboard_markups = InlineKeyboardMarkup(main_keyboard)
