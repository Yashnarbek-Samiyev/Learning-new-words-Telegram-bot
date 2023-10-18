import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, CallbackQueryHandler, MessageHandler, Filters
from bot import config
from bot.handlers import user
from bot.handlers import word
from bot.keyboards import user as user_keyboard
from bot import states
# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(config.TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', user.start),
            CommandHandler('add', user.add_word),
            CommandHandler('learn', user.learn),
            CommandHandler('repeat', user.repeat),
            CommandHandler('memorize', user.memorize),
            CallbackQueryHandler(
                word.new_words_start, pattern=user_keyboard.NEW_WORDS_KEY),
            CallbackQueryHandler(
                word.new_words_update, pattern='^known-'),
            CallbackQueryHandler(
                word.new_words_update, pattern='^learn-'),
            CallbackQueryHandler(
                word.review_words_start, pattern=user_keyboard.REVIEW_KEY),
            CallbackQueryHandler(
                word.review_words_update, pattern='^review_known-'),
            CallbackQueryHandler(
                word.review_words_update, pattern='^review_learn-'),
            CallbackQueryHandler(
                word.settings_start, pattern=user_keyboard.SETTINGS_KEY),
            CallbackQueryHandler(
                word.settings_start, pattern='^dictionary'),
            CallbackQueryHandler(
                word.settings_update, pattern='^language'),
            CallbackQueryHandler(
                word.back_start, pattern='^back'),
            CallbackQueryHandler(
                word.back_update, pattern='^back'),
            CallbackQueryHandler(
                word.check_word, pattern='^check-'),
            CallbackQueryHandler(
                user.start, pattern='add_cancel'),
            CallbackQueryHandler(
                word.add_new_word, pattern='add_approve'),
        ],
        states={
            LEARNING: [CommandHandler('learn', learn)],
            REPEATING: [CommandHandler('repeat', repeat)],
            states.SETTINGS: [
                CallbackQueryHandler(
                    word.settings_start, pattern='^dictionary'),
                CallbackQueryHandler(
                    word.settings_update, pattern='^language'),
                CallbackQueryHandler(
                    word.back_start, pattern='^back'),],
            states.NEW: [
                CallbackQueryHandler(
                    word.cancel_word, pattern='add_cancel'),
                CallbackQueryHandler(
                    word.add_new_word, pattern='add_approve'),
                MessageHandler(Filters.all, word.add_word),],

        },
        fallbacks=[CommandHandler('start', user.start),],
    )

    dispatcher.add_handler(conv_handler)
    # on different commands - answer in Telegram

    # Start the Bot
    updater.start_polling()
    updater.idle()
