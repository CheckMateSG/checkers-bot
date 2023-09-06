import logging
import time
from credentials import BOT_TOKEN, URL
from messages import START, ONBOARD_START, WIKI, ONBOARD_REPLY, ONBOARD_TEST, ERROR, ONBOARD_DONE, PRIVACY_POLICY, QUIZ

import flask

from telebot import TeleBot, types, logger
from telebot.util import quick_markup

API_TOKEN = BOT_TOKEN

# WEBHOOK_HOST = URL
# WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
# WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

# WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
# WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# # Quick'n'dirty SSL certificate generation:
# #
# # openssl genrsa -out webhook_pkey.pem 2048
# # openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
# #
# # When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# # with the same value in you put in WEBHOOK_HOST

# WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
# WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = logger
logger.setLevel(logging.INFO)

bot = TeleBot(API_TOKEN)

# app = flask.Flask(__name__)

# # Empty webserver index, return nothing, just http 200
# @app.route('/', methods=['GET', 'HEAD'])
# def index():
#     return ''


# # Process webhook calls
# @app.route(WEBHOOK_URL_PATH, methods=['POST'])
# def webhook():
#     if flask.request.headers.get('content-type') == 'application/json':
#         json_string = flask.request.get_data().decode('utf-8')
#         update = types.Update.de_json(json_string)
#         bot.process_new_updates([update])
#         return ''
#     else:
#         flask.abort(403)


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

#deactivate command

bot.infinity_polling()


#webhook set up below

# # Remove webhook, it fails sometimes the set if there is a previous webhook
# bot.remove_webhook()

# time.sleep(0.1)

# # Set webhook
# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
#                 certificate=open(WEBHOOK_SSL_CERT, 'r'))

# # Start flask server
# app.run(host=WEBHOOK_LISTEN,
#         port=WEBHOOK_PORT,
#         ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
#         debug=True)