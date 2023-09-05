import logging
import time
from credentials import BOT_TOKEN, URL
from messages import START, ONBOARD, INFO_LINK, ONBOARD_REPLY, ERROR

import flask

from telebot import TeleBot, types, logger

API_TOKEN = BOT_TOKEN

WEBHOOK_HOST = URL
WEBHOOK_PORT = 8443  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '0.0.0.0'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

# Quick'n'dirty SSL certificate generation:
#
# openssl genrsa -out webhook_pkey.pem 2048
# openssl req -new -x509 -days 3650 -key webhook_pkey.pem -out webhook_cert.pem
#
# When asked for "Common Name (e.g. server FQDN or YOUR name)" you should reply
# with the same value in you put in WEBHOOK_HOST

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = logger
logger.setLevel(logging.INFO)

bot = TeleBot(API_TOKEN)

app = flask.Flask(__name__)

def gen_markup(row_width):
    markup = types.InlineKeyboardMarkup()
    markup.row_width = row_width
    markup.add(types.InlineKeyboardButton("Yes", callback_data="cb_yes"),
                               types.InlineKeyboardButton("No", callback_data="cb_no"))
    return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_yes":
        bot.answer_callback_query(call.id, "Answer is Yes")
    elif call.data == "cb_no":
        bot.answer_callback_query(call.id, "Answer is No")

@bot.message_handler(func=lambda message: True)
def message_handler(message):
    bot.send_message(message.chat.id, "Yes/no?", reply_markup=gen_markup())


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


# Handle '/start' - to add logic for activating message receiving
@bot.message_handler(commands=['start'])
def send_start(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, START)

#handle '/onboard'   
@bot.message_handler(commands=['onboard'])
def send_onboard(message):
    chat_id = message.chat.id
    #users must reply to this message
    markup = types.ForcedReply(selective=False)
    bot.send_message(chat_id,ONBOARD, reply_markup=markup)
    

#handle '/info'
@bot.message_handler(commands=['info'])
def send_info(message):
    chat_id = message.chat.id
    bot.send_message(chat_id,INFO_LINK)
    

# Handle all other messages
@bot.message_handler(func=lambda message: True, content_types=['text'])
def reply_message(message):
    if message.reply_to_message.text == ONBOARD:
        chat_id = message.chat.id
        markup = types.InlineKeyboardMarkup(types.InlineKeyboardButton("Got it!", callback_data="done"))
        bot.send_message(chat_id, ONBOARD_REPLY.format(message.text), reply_markup = markup)

    else:
        bot.reply_to(message, ERROR)


# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(0.1)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)