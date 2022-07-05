import random
from telegram import Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
import os.path
TOKEN = 'YOUR TOKEN HERE'  # Don't forget input your token

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
number_of_candies = 10


def start(update, context):
    context.bot.send_message(update.effective_chat.id, f"""Hello, mate! This game names 'Candies'.
    We have {number_of_candies} candies.
    You and I will take turns taking from 1 to 3 candies.
    The one who takes the last coin loses.
    To take candies enter number. You can see that information again using /info""")

def info(update, context):
    context.bot.send_message(update.effective_chat.id, f"""At game start we have {number_of_candies} candies.
    You and I will take turns taking from 1 to 3 candies.
    Lose someone who takes the last candy.
    To take candies enter number. 
    
    You can see that information again using /info""")


def get_message(update, context):
    text = update.message.text
    user_id = update.message.from_user.id

    if os.path.exists(f'users/{user_id}.txt') is False:
        with open(f'users/{user_id}.txt', 'w') as data:
            data.write(str(number_of_candies))
            data.close()

    with open(f'users/{user_id}.txt', 'r') as data:
        candies = int(data.read())
        data.close()
    max_candies = 3 if candies > 3 else candies
    if str(text).isdigit() and 0 < int(text) < 4 and int(text) <= candies:
        candies -= int(text)
        if candies == 0:
            context.bot.send_message(update.effective_chat.id, 'You Lose :(')
            os.remove(f'users/{user_id}.txt')
        else:
            bot_takes = bot_turn(candies)
            candies -= bot_takes
            if candies == 0:
                context.bot.send_message(update.effective_chat.id, f'Bot takes the last candy. You Win :)')
                os.remove(f'users/{user_id}.txt')
            else:
                context.bot.send_message(update.effective_chat.id, f"Bot takes {bot_takes} candies.\n "
                                                                   f"There are {candies} candies")
                with open(f'users/{user_id}.txt', 'w') as data:
                    data.write(str(candies))
                    data.close()
    else:
        if max_candies == 1:
            context.bot.send_message(update.effective_chat.id, f"There is only 1 candy. It seems you lose =( Take it "
                                                               f"anyway")
        else:
            context.bot.send_message(update.effective_chat.id, f"You can only take from 1 to {max_candies} candies "
                                                           f"or send /info to get information")


def bot_turn(candies):
    bot = (candies - 1) % 4
    if bot != 0:
        return bot
    else:
        max_candies = 3 if candies > 3 else candies
        return random.randint(1, max_candies)



start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
message_handler = MessageHandler(Filters.text, get_message)
unknown_handler = MessageHandler(Filters.command, info)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(message_handler)

if os.path.isdir('users') is False:
    os.mkdir("users")
print('server started')
updater.start_polling()
updater.idle()