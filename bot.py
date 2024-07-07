# Classes from telegram used for handling updates, buttons, and keyboards in Telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

# Classes from telegram.ext providing convenient tools for handling commands,
# messages, and interacting with users
from telegram.ext import (Application, CommandHandler, CallbackQueryHandler,
                          CallbackContext, ConversationHandler)

from urllib.parse import urlencode, parse_qs

# Import questions from the question module
from question import questions

# Import bot token
from const import YOUR_TELEGRAM_API_TOKEN

# Bot token
YOUR_TELEGRAM_API_TOKEN = YOUR_TELEGRAM_API_TOKEN

# Finite state machine states
CHOOSING_TOPIC, CHOOSING_QUESTION, CHOOSING_ANSWER = range(3)

# Flag to control the bot's state
bot_active = True

# Handler for the /start command
async def start(update: Update, context: CallbackContext) -> int:
    global bot_active
    bot_active = True
    await update.message.reply_text(
        "Hello! I am a bot for testing knowledge in QA automation.\n"
        "Choose a topic to start the quiz:",
        reply_markup=get_topics_keyboard(),
    )
    return CHOOSING_TOPIC


# Function to stop the bot
async def stop(update: Update, context: CallbackContext) -> None:
    global bot_active
    bot_active = False
    await update.message.reply_text("Bot stopped. Use /start to restart.")
    return ConversationHandler.END

# Generate keyboard with topic selection
def get_topics_keyboard():
    keyboard = [
        [InlineKeyboardButton(topic, callback_data=topic)] for topic in
        questions.keys()
    ]
    return InlineKeyboardMarkup(keyboard)


# Handler for choosing a topic
async def choose_topic(update: Update, context: CallbackContext) -> int:
    global bot_active
    if not bot_active:
        await update.callback_query.answer(
            "Bot stopped. Use /start to restart.")
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()
    topic = query.data
    context.user_data['topic'] = topic
    await query.edit_message_text(
        f'You have chosen the topic: {topic}\n'
        'Choose a question to test your knowledge:',
        reply_markup=get_questions_keyboard(topic),
    )
    return CHOOSING_QUESTION


# Function to generate keyboard with questions
def get_questions_keyboard(topic):
    keyboard = []
    for index, question in enumerate(questions[topic], start=1):
        keyboard.append([
            InlineKeyboardButton(
                question['question'],
                callback_data=urlencode({"question_index": str(index)})
            )
        ])
    keyboard.append([
        InlineKeyboardButton("Return to the list of topics",
                             callback_data="back_to_topics")
    ])
    return InlineKeyboardMarkup(keyboard)


# Function to handle choosing a question
async def choose_question(update: Update, context: CallbackContext) -> int:
    global bot_active
    if not bot_active:
        await update.callback_query.answer(
            "Bot stopped. Use /start to restart.")
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()

    if query.data == "back_to_questions":
        topic = context.user_data['topic']
        await query.edit_message_text(
            'Choose a question to test your knowledge:',
            reply_markup=get_questions_keyboard(topic),
        )
        return CHOOSING_QUESTION
    elif query.data == "back_to_topics":
        await back_to_topics(update, context)
        return CHOOSING_TOPIC

    query_data = parse_qs(query.data)
    try:
        question_index = int(query_data["question_index"][0]) - 1
        topic = context.user_data['topic']
        question_data = questions[topic][question_index]
        context.user_data['question_data'] = question_data
        await query.edit_message_text(
            f'You have chosen the question: {question_data["question"]}\n'
            'Choose an answer:',
            reply_markup=get_answers_keyboard(question_data),
        )
        return CHOOSING_ANSWER
    except (KeyError, ValueError, IndexError):
        await query.edit_message_text("Error: question not found.")
        return CHOOSING_QUESTION


# Generate keyboard with answer options for the selected question
def get_answers_keyboard(question_data):
    keyboard = [
        [InlineKeyboardButton(option, callback_data=option)] for option in
        question_data['options']
    ]
    return InlineKeyboardMarkup(keyboard)


# Handler for choosing an answer
async def choose_answer(update: Update, context: CallbackContext) -> int:
    global bot_active
    if not bot_active:
        await update.callback_query.answer(
            "Bot stopped. Use /start to restart.")
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()
    selected_option = query.data
    correct_answer = context.user_data['question_data']['correct']
    if selected_option == correct_answer:
        await query.edit_message_text(
            f'Correct! Answer: {selected_option}',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                "Return to the list of questions",
                callback_data="back_to_questions")]])
        )
    else:
        await query.edit_message_text(
            f'Incorrect. Correct answer: {correct_answer}',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                "Return to the list of questions",
                callback_data="back_to_questions")]])
        )
    return CHOOSING_QUESTION


# Handler for returning to the list of questions
async def back_to_questions(update: Update, context: CallbackContext) -> int:
    global bot_active
    if not bot_active:
        await update.callback_query.answer(
            "Bot stopped. Use /start to restart.")
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()
    topic = context.user_data['topic']
    await query.edit_message_text(
        'Choose a question to test your knowledge:',
        reply_markup=get_questions_keyboard(topic),
    )
    return CHOOSING_QUESTION


# Handler for returning to the list of topics
async def back_to_topics(update: Update, context: CallbackContext) -> int:
    global bot_active
    if not bot_active:
        await update.callback_query.answer(
            "Bot stopped. Use /start to restart.")
        return ConversationHandler.END

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        'Choose a topic to start the quiz:',
        reply_markup=get_topics_keyboard(),
    )
    return CHOOSING_TOPIC


def main() -> None:
    app = Application.builder().token(YOUR_TELEGRAM_API_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_TOPIC: [CallbackQueryHandler(choose_topic)],
            CHOOSING_QUESTION: [
                CallbackQueryHandler(choose_question),
                CallbackQueryHandler(back_to_questions,
                                     pattern='back_to_questions')
            ],
            CHOOSING_ANSWER: [CallbackQueryHandler(choose_answer)],
        },
        fallbacks=[CommandHandler('start', start)]
    )

    app.add_handler(conv_handler)

    # Add handler for the /stop command
    app.add_handler(CommandHandler("stop", stop))

    app.run_polling()


if __name__ == '__main__':
    main()
