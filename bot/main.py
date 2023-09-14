import logging
import time
from credentials import BOT_TOKEN
from messages import START, ONBOARD_START, WIKI, ONBOARD_REPLY, ONBOARD_TEST, ERROR, ONBOARD_DONE, PRIVACY_POLICY, QUIZ

from flask import Flask, request, Response

from telebot import TeleBot, types, logger
from telebot.util import quick_markup

API_TOKEN = BOT_TOKEN

logger = logger
logger.setLevel(logging.INFO)

bot = TeleBot(API_TOKEN)

app = Flask(__name__)

# # Empty webserver index, return nothing, just http 200
# @app.route('/', methods=['GET', 'HEAD'])
# def index():
#     return ''

# Process webhook calls
@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return Response('ok', status=200)
    else:
        return "<h1>Welcome!</h1>"

# Handle '/start' - to add logic for activating message receiving
@bot.message_handler(commands=['start'])
def send_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, START)

#handle '/onboard'   
@bot.message_handler(commands=['onboard'])
def send_onboard(message):
    chat_id = message.chat.id
    #users must reply their name to this message
    markup = types.ForceReply(selective=True)
    bot.send_message(chat_id,ONBOARD_START, reply_markup=markup)

#handle '/info'
@bot.message_handler(commands=['info'])
def send_info(message):
    chat_id = message.chat.id
    markup = quick_markup({
            'Privacy Policy': {'url': PRIVACY_POLICY},
            'Wiki Page': {'url': WIKI}}, 
            row_width=1)
    bot.send_message(chat_id,"Check out below for our resources!", reply_markup=markup)

#handle '/deactivate' - to include closing message portal
@bot.message_handler(commands=['deactivate'])
def send_info(message):
    chat_id = message.chat.id
    markup = quick_markup({
            'I am ready!': {'callback_data': 'Start message portal'}}, 
            row_width=1)
    bot.send_message(chat_id,"Sorry to see you go, join back anytime you're ready!", reply_markup=markup)
    

# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def reply_message(message):
    #if user replies name
    if message.reply_to_message.text == ONBOARD_START:
        chat_id = message.chat.id
        markup = quick_markup({
            'Privacy Policy': {'url': PRIVACY_POLICY},
            'Got it!': {'callback_data': 'Understood privacy terms'}}, 
            row_width=1)
        bot.send_message(chat_id, ONBOARD_REPLY.format(name = message.text), reply_markup = markup)
    #if user replies plain text
    else:
        bot.reply_to(message, ERROR)

#handles callback queries from inline keyboard buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "Understood privacy terms":
        markup = quick_markup({"Take me to quiz!":{"url": QUIZ},
                               "I've done the quiz!": {"callback_data":"Quiz done"}}, 
                               row_width=1)
        # bot.answer_callback_query(call.id, ONBOARD_TEST, reply_markup = markup)
        # bot.edit_message_text(ONBOARD_TEST, call.message.chat.id, call.message.id,reply_markup=markup)
        bot.send_message(call.from_user.id, ONBOARD_TEST, reply_markup=markup)
    elif call.data == "Quiz done":
        bot.send_message(call.from_user.id, ONBOARD_DONE)

# Start flask server
if __name__ == "__main__":
    app.run(port=8443, debug=True)