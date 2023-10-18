
from telegram import Update,  User
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters, Updater
from db.functions.user import register
from db import table
from bot.keyboards.user import main_keyboard_markup
from bot.keyboards.settings import main_keyboard_markups
from bot import states
from telegram import ParseMode
import random


user_data = {}

LEARN_LIMIT = 10

LEARNING, REPEATING = range(2)


def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_channel_id = "1001005582487"

    user_in_channel = user_id in context.bot.get_chat_member(
        user_channel_id, user_id).user.username is not None

    if user_in_channel:
        update.message.reply_text(
            "You are already a member of the channel. You can now use the bot for word memorization.")
    else:
        update.message.reply_text(
            f"Welcome to the Word Memorization Bot! To get started, please join our channel {user_channel_id}. Once you've joined, send /memorize to start memorizing words.")

    user: User = update.effective_user
    register(user.id, user.first_name,
             user.last_name)
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'learned_words': set(), 'repeatable_words': set()}

    update.message.reply_text(
        "You are in main menu",
        reply_markup=main_keyboard_markup
    )

    return ConversationHandler.END

# ======takrorlashda 3talik pag'ona qilinsin, 3 marta to'g'ri topgandan so'ng so'z eslab qolidi deb qabul qilinsin va qayta u suz chiqarilmasin


word_repetition_counts = {}


def memorize(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    word = table.WordsTable.word

    if user_id not in word_repetition_counts:
        word_repetition_counts[user_id] = {word: 1}
    elif word not in word_repetition_counts[user_id]:
        word_repetition_counts[user_id][word] = 1
    else:
        word_repetition_counts[user_id][word] += 1

    if word_repetition_counts[user_id][word] < 3:
        update.message.reply_text(
            f"Memorize this word: {word}. You've repeated it {word_repetition_counts[user_id][word]} times.")
    else:
        update.message.reply_text(
            f"Congratulations! You've successfully memorized the word: {word}.")
        del word_repetition_counts[user_id][word]


# ================================================================== Limit daily words

def learn(update, context):
    user_id = update.effective_user.id
    user_words = user_data[user_id]

    if len(user_words['learned_words']) >= LEARN_LIMIT:
        update.message.reply_text(
            "You have already learned your limit of words for today.")
        return ConversationHandler.END
    user_words['learned_words'].add(word_to_learn)
    update.message.reply_text(f"You learned a new word: {word_to_learn}")
    return REPEATING


def repeat(update, context):
    user_id = update.effective_user.id
    user_words = user_data[user_id]
    if not user_words['learned_words']:
        update.message.reply_text(
            "You haven't learned any words yet. Type /learn to start learning.")
        return ConversationHandler.END
    word_to_repeat = random.choice(list(user_words['learned_words']))
    update.message.reply_text(f"Repeat this word: {word_to_repeat}")
    return REPEATING

# ================================================================== Settings


def back(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    start(update, context)
    return ConversationHandler.END


def add_word(update: Update, context: CallbackContext) -> None:

    update.message.reply_text(
        "Yangi so'zni kiriting\n\n<b>so'z</b>\n<i>tarjima</i>\n\nSo'zni rasm orqali yoki rasm kiritimsadan kiritish mumkin.",
        parse_mode=ParseMode.HTML
    )

    return states.NEW
