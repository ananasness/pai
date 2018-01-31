import re

import telebot
from telebot import types

from gomoku import Gomoku
from matches import Matches
from minmax_alg import MinMax

with open('C:\\Users\\Baldur\\Desktop\\pai\\tic-tac-toe\\token', 'r') as tokenfile:
    TOKEN = tokenfile.read()

bot = telebot.TeleBot(TOKEN)
tictactoe = {}
fiveinarow = {}
matches = {}
equation_message_ids = {}


def reset_objects(chat_id):
    for obj in [tictactoe, fiveinarow, matches, equation_message_ids]:
        obj.pop(chat_id, None)


@bot.message_handler(commands=['start', 'end', 'reset', 'quit', 'stop', 'exit'])
def main_menu(message):
    reset_objects(message.chat.id)
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


@bot.callback_query_handler(func=lambda call: call.data.startswith("equation"))
def callback_inline(call):
    global equation_message_ids
    if call.message:
        if call.data == "equation start":
            markup = types.ForceReply(selective=False)
            equation_message_ids[call.message.chat.id] = bot.send_message(call.message.chat.id, "Enter your equation:",
                                                                          reply_markup=markup).message_id


@bot.message_handler(func=lambda message: message.reply_to_message and message.chat.id in equation_message_ids and
                                          message.reply_to_message.message_id == equation_message_ids[message.chat.id])
def test(message):
    bot.send_message(message.chat.id, "This is the response! Your request was:\n%s" % message.text)


@bot.callback_query_handler(func=lambda call: call.data.startswith("tictactoe"))
def callback_inline(call):
    if call.message:
        if call.data == "tictactoe start":
            tictactoe[call.message.chat.id] = MinMax()

            board = [tictactoe[call.message.chat.id].board[i * 3: (i + 1) * 3] for i in range(3)]
            markup = create_gomoku_keyboard(3, "tictactoe", board)
            bot.send_message(call.message.chat.id, "Make your move!", reply_markup=markup)
        elif call.message.chat.id in tictactoe:
            search = re.search("tictactoe ([0-9]):([0-9])", call.data)
            if search:
                move = int(search.group(1)) + int(search.group(2)) * 3
                if tictactoe[call.message.chat.id].valid(move):
                    result = tictactoe[call.message.chat.id].play2(move)
                    board = [result[0].replace('\n', '')[i * 3: (i + 1) * 3] for i in range(3)]
                    send_gamoku_info(call, board, 3, "tictactoe")
                    if result[1]:
                        message = "You won! 😻"
                        if result[1] == 1:
                            message = "You lost! 😈"
                        if result[1] == 3:
                            message = "It's a draw! 😱"
                        send_end_game_info(call, message, "tictactoe")


@bot.callback_query_handler(func=lambda call: call.data.startswith("fiveinarow"))
def callback_inline(call):
    if call.message:
        if call.data == "fiveinarow start":
            fiveinarow[call.message.chat.id] = Gomoku()
            send_gamoku_info(call, fiveinarow[call.message.chat.id].state, 8, "fiveinarow")
        elif call.message.chat.id in fiveinarow:
            search = re.search("fiveinarow ([0-9]):([0-9])", call.data)
            if search:
                x, y = int(search.group(1)), int(search.group(2))
                if fiveinarow[call.message.chat.id].is_move_valid(x, y):
                    result = fiveinarow[call.message.chat.id].play(x, y)
                    send_gamoku_info(call, result, 8, "fiveinarow")


@bot.callback_query_handler(func=lambda call: call.data.startswith("matches"))
def callback_inline(call):
    global matches
    if call.message:
        if call.data == "matches start":
            matches[call.message.chat.id] = Matches()
            send_matches_info(call, matches[call.message.chat.id].state)
        elif call.message.chat.id in matches:
            search = re.search("matches ([0-9])", call.data)
            if search:
                new_state = matches[call.message.chat.id].state - int(search.group(1))
                if matches[call.message.chat.id].state_valid(new_state):
                    if matches[call.message.chat.id].play(new_state):
                        send_end_game_info(call, "You lost! 😈", "matches")
                    else:
                        send_matches_info(call, matches[call.message.chat.id].state)


def create_gomoku_keyboard(size, game, board):
    markup = types.InlineKeyboardMarkup()
    for i in range(size):
        buttons = [types.InlineKeyboardButton(
            text=board[i][buttonId],
            callback_data="%s %d:%d" % (game, buttonId, i)
        ) for buttonId in range(size)]
        markup.row(*buttons)
    return markup


def send_gamoku_info(call, board, size, game):
    markup = create_gomoku_keyboard(size, game, board)
    if call.data == game + " start":
        bot.send_message(call.message.chat.id, "Make your move!", reply_markup=markup)
    else:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "menu")
def callback_inline(call):
    if call.message:
        main_menu(call.message)


def send_matches_info(call, state):
    global matches
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text="Take one match", callback_data="matches 1")]
    if state > 1:
        buttons.append(types.InlineKeyboardButton(text="Take two matches", callback_data="matches 2"))
    if state > 2:
        buttons.append(types.InlineKeyboardButton(text="Take three matches", callback_data="matches 3"))
    for button in buttons:
        markup.add(button)
    if call.data == "matches start":
        bot.send_message(call.message.chat.id, "There are %d matches.\nMake your move!" % state, reply_markup=markup)
    else:
        bot.edit_message_text("There are %d matches.\nMake your move!" % state, call.message.chat.id,
                              call.message.message_id, reply_markup=markup)


def send_end_game_info(call, text, game):
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text="Replay", callback_data="%s start" % game),
               types.InlineKeyboardButton(text="Menu", callback_data="menu")]
    for button in buttons:
        markup.add(button)
    bot.send_message(call.message.chat.id, text, reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
