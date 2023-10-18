
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from db.functions.user import register
from db.functions.word import get_user_word, users_words_create, get_user_review_word, users_words_update, get_word_by_id, word_create
from db.functions.user import get_user_data
from bot.keyboards.word import make_word_inline_keyboard
from bot.keyboards.user import main_keyboard_markup
from bot.keyboards.settings import main_keyboard_markups

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def new_words_start(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    user = get_user_data(query.from_user.id)
    word = get_user_word(user.id)

    if word:
        query.edit_message_text(
            text=f"{word.word}", reply_markup=make_word_inline_keyboard(word, user))
    else:
        query.edit_message_text(text="No words")


def new_words_update(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')
    query.answer()
    if len(data) > 3:
        users_words_create(data[2], data[1], data[3])
    user = get_user_data(query.from_user.id)
    word = get_user_word(user.id)
    if word:
        query.edit_message_text(
            text=f"{word.word}", reply_markup=make_word_inline_keyboard(word, user))
    else:
        query.edit_message_text(text="No words")


def review_words_start(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    query.answer()
    user = get_user_data(query.from_user.id)
    word = get_user_review_word(user.id)
    if word:
        query.edit_message_text(
            text=f"{word.word}", reply_markup=make_word_inline_keyboard(word, user, "review_"))
    else:
        query.edit_message_text(text="No words")


def review_words_update(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')
    query.answer()
    if len(data) > 3:
        users_words_update(data[2], data[1], data[3])
    user = get_user_data(query.from_user.id)
    word = get_user_word(user.id)

    if word:
        query.edit_message_text(
            text=f"{word.word}", reply_markup=make_word_inline_keyboard(word, user, "review_"))
    else:
        query.edit_message_text(text="No words")
# ================Settings===================


def settings_start(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="You are in settings menu",
                            reply_markup=main_keyboard_markups)


def settings_update(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="You are in settings menu",
                            reply_markup=main_keyboard_markups)


def back_start(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="You are in main menu",
                            reply_markup=main_keyboard_markup)


def back_update(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="You are in main menu",
                            reply_markup=main_keyboard_markup)
# ============================================


def check_word(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    data = query.data.split('-')
    word = get_word_by_id(data[1])
    query.answer(word.word_translation, show_alert=True)


def add_word(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [
            InlineKeyboardButton("❌",
                                 callback_data="add_cancel"), InlineKeyboardButton("✅",  callback_data="add_approve")
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.copy(chat_id=update.message.chat.id,
                        reply_markup=reply_markup),


def cancel_word(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    message = query.message
    query.delete_message()
    context.bot.send_message(
        chat_id=message.chat.id, text="So'z qo'shish bekor qilindi")

    return ConversationHandler.END


def add_new_word(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    message = query.message

    photo = None
    if message.photo:
        text = message.caption
        photo = message.photo[-1].file_id
    else:
        text = message.text
    text = text.split('\n')
    word = text[0]
    word_translation = text[1]
    word_create(word, word_translation, photo)
    query.delete_message()

    context.bot.send_message(
        chat_id=message.chat.id, text="So'z muvaffaqiyatli qo'shildi")

    return ConversationHandler.END
