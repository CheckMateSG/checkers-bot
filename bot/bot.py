from telegram import Bot
from telegram.ext import Application
from credentials import BOT_TOKEN

application = Application.builder().token(BOT_TOKEN).build()
    
# Register handlers here

# Get the update_queue from which the application fetches the updates to handle
update_queue = application.update_queue
start_fetching_updates(update_queue) #placeholder for webhook setup

# Start and run the application
async with application:
    application.start()
    # when some shutdown mechanism is triggered:
    application.stop()