from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
# from credentials import BOT_TOKEN, URL
from flask import Flask, request, Response
import requests
import json


app = Flask(__name__)

BOT_TOKEN = '6544110821:AAHsLzgKUu3rWQkTfLTd4bYUlN4vyMRQRO8'


#commands
@app.route("/{}".format(BOT_TOKEN), methods=["POST"])
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    msg = "Hello, I'm a bot! Activate receiving messages!"
    # now just send the message back
    # notice how we specify the chat and the msg we reply to
    await update.message.reply_text(msg)
    return "ok"


@app.route("/{}".format(BOT_TOKEN), methods=["POST"])
async def onboard(update: Update):
    user = update.message.from_user
    msg = "Hello, begin onboarding now!"

    await update.message.reply_text(msg)
    return "ok"

#handle errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(BOT_TOKEN).build()

    # Commands
    application.add_handler(CommandHandler(command="start", callback=start))
    application.add_handler(CommandHandler(command="onboard", callback=onboard))

    #Errors
    application.add_error_handler(error)
    
    application.run()


if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
