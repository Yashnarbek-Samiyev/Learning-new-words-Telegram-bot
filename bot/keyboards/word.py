# inline keyboard
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

NEW_WORDS_KEY = "new_words"
REVIEW_KEY = "review_words"
SETTINGS_KEY = "settings"

word_keyboard = [
    [
        InlineKeyboardButton("📚 Learning new words",
                             callback_data=NEW_WORDS_KEY),
    ],
    [InlineKeyboardButton("📖 Review words", callback_data=REVIEW_KEY)],
    [InlineKeyboardButton("⚙️ Settings", callback_data=SETTINGS_KEY)],
]

word_keyboard_markup = InlineKeyboardMarkup(word_keyboard)


def make_word_inline_keyboard(word, user, prefix=""):
    word_keyboard = [
        [
            InlineKeyboardButton(
                "✅ Known", callback_data=f"{prefix}known-{word.id}-{user.id}-1"),
            InlineKeyboardButton(
                "♻️ Learn", callback_data=f"{prefix}learn-{word.id}-{user.id}-2"),
        ], [
            InlineKeyboardButton(
                "🧐 Check", callback_data=f"check-{word.id}"),


        ],

    ]

    word_keyboard_markup = InlineKeyboardMarkup(word_keyboard)
    return word_keyboard_markup
