from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
import random

user_data = {}

LEARN_LIMIT = 10

LEARNING, REPEATING = range(2)


def start(update, context):
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {
            'learned_words': set(), 'repeatable_words': set()}

    update.message.reply_text(
        "Welcome to the Word Learning Bot! Type /learn to start learning.")


def learn(update, context):
    user_id = update.effective_user.id
    user_words = user_data[user_id]

    # Check if the user has reached the daily limit
    if len(user_words['learned_words']) >= LEARN_LIMIT:
        update.message.reply_text(
            "You have already learned your limit of words for today.")
        return ConversationHandler.END

    # Implement your word learning logic here
    # For example, you can fetch a random word to learn
    word_to_learn = "ExampleWord"  # Replace with your logic to get a word

    user_words['learned_words'].add(word_to_learn)
    update.message.reply_text(f"You learned a new word: {word_to_learn}")

    return REPEATING


def repeat(update, context):
    user_id = update.effective_user.id
    user_words = user_data[user_id]

    # Check if the user has words to repeat
    if not user_words['learned_words']:
        update.message.reply_text(
            "You haven't learned any words yet. Type /learn to start learning.")
        return ConversationHandler.END

    # Implement your word repeating logic here
    # For example, you can fetch a random word to repeat
    word_to_repeat = random.choice(list(user_words['learned_words']))

    update.message.reply_text(f"Repeat this word: {word_to_repeat}")

    return REPEATING


def main():
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    dispatcher = updater.dispatcher

    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            LEARNING: [CommandHandler('learn', learn)],
            REPEATING: [CommandHandler('repeat', repeat)],
        },
        fallbacks=[],
    )

    dispatcher.add_handler(conversation_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
