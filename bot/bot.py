from telegram import Update
from telegram.ext import Application, CommandHandler
from credentials import BOT_TOKEN, URL
from flask import Flask, request


app = Flask(__name__)


# # Get the update_queue from which the application fetches the updates to handle
# update_queue = application.Updater().update_queue

@app.route("/{}".format(BOT_TOKEN), methods=["POST"])
async def start(update: Update):

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


# @app.route('/setwebhook', methods=['GET', 'POST'])
# def set_webhook():
#     # we use the bot object to link the bot to our app which live
#     # in the link provided by URL
#     s = application.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=BOT_TOKEN))
#     # something to let us know things work
#     if s:
#         return "webhook setup ok"
#     else:
#         return "webhook setup failed"


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("TOKEN").build()

    # Register handlers here
    application.add_handler(CommandHandler(command="start", callback=start))
    application.add_handler(CommandHandler(command="onboard", callback=onboard))


    application.start_webhook(
        listen="0.0.0.0",
        port=80,
        # key="private.key",
        # cert="cert.pem",
        webhook_url="https://a826-2404-e801-2003-29a-f18f-cf73-a1e7-76ce.ngrok-free.app",
    )
    
    application.run()


if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
