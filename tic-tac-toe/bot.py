import re

import telebot
from telebot import types

from matches import Matches

with open('C:\\Users\\Baldur\\Desktop\\pai\\tic-tac-toe\\token', 'r') as tokenfile:
    TOKEN = tokenfile.read()

bot = telebot.TeleBot(TOKEN)
matches = None


@bot.message_handler(commands=['start', 'help'])
def main_menu(message):
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="⚡ Source code on GitHub ⚡",
                                   url="https://github.com/ananasness/pai"),
        types.InlineKeyboardButton(text="🍒 Play tic-tac-toe 🍒", callback_data="tictactoe start"),
        types.InlineKeyboardButton(text="🍄 Play matches 🍄", callback_data="matches start"),
        types.InlineKeyboardButton(text="🌶 Play 5-in-a-row 🌶", callback_data="fiveinarow start"),
        types.InlineKeyboardButton(text="✍️ Solve equation ✍️", callback_data="equation start")
    ]
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, """Hey there! I'm Super AI Bot 🤖 
I can play some games with you or solve your math equation. 
What do you want me to do?""",
                     reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("tictactoe") or call.data.startswith("fiveinarow"))
def callback_inline(call):
    if call.message:
        if call.data == "tictactoe start":
            markup = create_gomoku_keyboard(3, 3, "tictactoe")
            bot.send_message(call.message.chat.id, "Make your move!", reply_markup=markup)
        elif call.data.startswith("tictactoe"):
            bot.send_message(call.message.chat.id, call.data)
            # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=)
        if call.data == "fiveinarow start":
            markup = create_gomoku_keyboard(8, 10, "fiveinarow")
            bot.send_message(call.message.chat.id, "Make your move!", reply_markup=markup)
        elif call.data.startswith("fiveinarow"):
            bot.send_message(call.message.chat.id, call.data)
            # bot.edit_message_text("kek", call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("matches"))
def callback_inline(call):
    global matches
    if call.message:
        if call.data == "matches start":
            matches = Matches()
            send_matches_info(call, matches.state)
        elif matches:
            search = re.search("matches ([0-9])", call.data)
            if search:
                new_state = matches.state - int(search.group(1))
                if matches.state_valid(new_state):
                    if matches.play(new_state):
                        send_matches_info(call, -1)
                    else:
                        send_matches_info(call, matches.state)


def create_gomoku_keyboard(rows, columns, game):
    markup = types.InlineKeyboardMarkup()
    for i in range(rows):
        buttons = [types.InlineKeyboardButton(
            text=".",
            callback_data="%s %d" % (game, (columns * i + buttonId))
        ) for buttonId in range(columns)]
        markup.row(*buttons)
    return markup


@bot.callback_query_handler(func=lambda call: call.data == "menu")
def callback_inline(call):
    if call.message:
        main_menu(call.message)


def send_matches_info(call, state):
    global matches
    if state == -1:
        matches = None
        send_end_game_info(call, "You lost! 😈", "matches")
        return
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text="Take one match", callback_data="matches 1")]
    if state > 1:
        buttons.append(types.InlineKeyboardButton(text="Take two matches", callback_data="matches 2"))
    if state > 2:
        buttons.append(types.InlineKeyboardButton(text="Take three matches", callback_data="matches 3"))
    for button in buttons:
        markup.add(button)
    bot.send_message(call.message.chat.id, "There are %d matches.\nMake your move!" % state, reply_markup=markup)


def send_end_game_info(call, text, game):
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text="Replay", callback_data="%s start" % game),
               types.InlineKeyboardButton(text="Menu", callback_data="menu")]
    for button in buttons:
        markup.add(button)
    bot.send_message(call.message.chat.id, text, reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
