import re
import shutil

import requests
import speech_recognition as sr
import telebot
import time
from googletrans import Translator
from telebot import types
from telebot.apihelper import ApiException
from telebot import apihelper

from features.obj_recognition import ObjRecognition
from features.text_command_parser import *
from features.audio_converter import *
from games.gomoku2 import Game as Gomoku
from games.matches import Matches
from games.minmax_alg import MinMax

with open('token', 'r') as tokenfile:
    TOKEN = tokenfile.read()
with open('wolfram_appid') as appidfile:
    WOLFRAM_APPID = appidfile.read()

PROXY = {'https': 'socks5://:@5.101.64.68:64897'}
apihelper.proxy = PROXY
bot = telebot.TeleBot(TOKEN, threaded=False)
translator = Translator()
obr = ObjRecognition()

tictactoe = {}
fiveinarow = {}
matches = {}
equation_message_ids = {}
translations = {}


def translate(chat_id, text):
    if chat_id in translations:
        translation = translator.translate(text, dest=translations[chat_id], src="en").text
        if translation is not None:
            return translation
    return text


def reset_objects(chat_id):
    for obj in [tictactoe, fiveinarow, matches, equation_message_ids]:
        obj.pop(chat_id, None)


@bot.message_handler(commands=['start', 'end', 'reset', 'quit', 'stop', 'exit'])
def main_menu(message):
    reset_objects(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="⚡ " + translate(message.chat.id, "Source code on GitHub") + " ⚡",
                                   url="https://github.com/ananasness/pai"),
        types.InlineKeyboardButton(text="🍒 " + translate(message.chat.id, "Play tic-tac-toe") + " 🍒",
                                   callback_data="tictactoe start"),
        types.InlineKeyboardButton(text="🍄 " + translate(message.chat.id, "Play the matches game") + " 🍄",
                                   callback_data="matches start"),
        types.InlineKeyboardButton(text="🌶 " + translate(message.chat.id, "Play 5-in-a-row") + " 🌶",
                                   callback_data="fiveinarow start"),
        types.InlineKeyboardButton(text="✍️ " + translate(message.chat.id, "Solve an equation") + " ✍️",
                                   callback_data="equation start"),
        types.InlineKeyboardButton(text="🇷🇺 " + translate(message.chat.id, "Translate") + " 🇺🇸",
                                   callback_data="translate start")
    ]
    for button in buttons:
        markup.add(button)
    text = translate(message.chat.id, "Hey there! I'm Super AI Bot") + " 🤖\n" + translate(message.chat.id, """
I can play some games with you or solve your math equation.
What do you want me to do?
Send me a voice message and tell me!
For now I only understand english speech...""")
    bot.send_message(message.chat.id, text=text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.startswith("translate"))
def translate_start(call):
    global translations
    if call.message:
        if call.data == "translate start":
            markup = types.InlineKeyboardMarkup()
            buttons = [
                types.InlineKeyboardButton(text="🇷🇺 Русский", callback_data="translate ru"),
                types.InlineKeyboardButton(text="🇺🇸 English", callback_data="translate en"),
                types.InlineKeyboardButton(text="🇫🇷 Français", callback_data="translate fr"),
                types.InlineKeyboardButton(text="🇪🇸 Español", callback_data="translate es"),
                types.InlineKeyboardButton(text="🇯🇵 日本語", callback_data="translate ja"),
                types.InlineKeyboardButton(text="🇺🇬 Do u no da wey?", callback_data="translate sw"),
                ]
            markup.add(*buttons[0:2])
            markup.add(*buttons[2:4])
            markup.add(*buttons[4:6])
            text = "Choose a language:"
            bot.send_message(call.message.chat.id, text=translate(call.message.chat.id, text), reply_markup=markup)
        else:
            search = re.search("translate ([a-zA-Z]{2})", call.data)
            if search:
                if search == "en":
                    if call.message.chat.id in translations:
                        translations.pop(call.message.chat.id, None)
                else:
                    translations[call.message.chat.id] = search.group(1)
            menu(call)


@bot.callback_query_handler(func=lambda call: call.data.startswith("equation"))
def equation_start(call):
    global equation_message_ids
    if call.message:
        if call.data == "equation start":
            markup = types.ForceReply(selective=False)
            equation_message_ids[call.message.chat.id] = bot.send_message(call.message.chat.id,
                                                                          text=translate(call.message.chat.id,
                                                                                         "Enter your equation:"),
                                                                          reply_markup=markup).message_id


@bot.message_handler(func=lambda message: message.reply_to_message and message.chat.id in equation_message_ids and
                                          message.reply_to_message.message_id == equation_message_ids[message.chat.id])
def solve_equation(message):
    payload = {"appid": WOLFRAM_APPID, "i": message.text}
    r = requests.get("http://api.wolframalpha.com/v1/simple", params=payload, stream=True)
    if r.status_code == 200:
        bot.send_photo(message.chat.id, r.raw)
    else:
        bot.send_message(message.chat.id,
                         text=translate(message.chat.id,
                                        "Oh no! There is something terribly wrong!\nI cannot help you at this time..."))
    send_end_game_info(message, translate(message.chat.id, "Would you like to try again?"), "equation",
                       translate(message.chat.id, "Solve another equation"))


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.send_message(message.chat.id, translate(message.chat.id, "I'm going to try to figure out what's on this picture you sent me..."))
    file_info = bot.get_file(message.photo[-1].file_id)
    # photo = bot.download_file(file_info.file_path)
    url = "https://api.telegram.org/file/bot{0}/{1}".format(TOKEN, file_info.file_path)
    r = requests.get(url, stream=True, proxies=PROXY)
    if r.status_code == 200:
        with open("photo.jpg", 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

        recognized = obr.get_info_about("photo.jpg")
    else:
        recognized = "Whoops..."
    bot.send_message(message.chat.id, translate(message.chat.id, recognized))



@bot.message_handler(content_types=['voice'])
def handle_audio(message):
    file_info = bot.get_file(message.voice.file_id)
    try:
        # voice_msg = bot.download_file(file_info.file_path)
        url = "https://api.telegram.org/file/bot{0}/{1}".format(TOKEN, file_info.file_path)
        voice_msg = requests.get(url, stream=True, proxies=PROXY).content

        temp_out_filename = "voice.flac"
        convert_to_flac(voice_msg, temp_out_filename)
        r = sr.Recognizer()
        with sr.AudioFile(temp_out_filename) as source:
            audio = r.record(source)
        os.remove(temp_out_filename)
        recognized_text = r.recognize_google(audio)
        command = command_parse(recognized_text)
        print(recognized_text, command)
        commands = {
            'tictactoe': "play tic-tac-toe",
            'matches': "play the matches game",
            'fiveinarow': "play 5-in-a-row",
            'equation': "solve an equation"
        }
        if command:
            send_end_game_info(message, translate(message.chat.id, "It looks like you want to " + commands[command]),
                               command, btn1_text=translate(message.chat.id, "Exactly!"))
        else:
            bot.send_message(message.chat.id, translate(message.chat.id, "I'm sorry. I didn't get that 0:"))


    except ApiException:
        print("Error downloading voice message from Telegram")
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


@bot.callback_query_handler(func=lambda call: call.data.startswith("tictactoe"))
def tictactoe_start(call):
    if call.message:
        if call.data == "tictactoe start":
            tictactoe[call.message.chat.id] = MinMax()

            markup = create_gomoku_keyboard(3, "tictactoe", MinMax.to_output(tictactoe[call.message.chat.id].board))
            bot.send_message(call.message.chat.id, translate(call.message.chat.id, "Make your move!"),
                             reply_markup=markup)
        elif call.message.chat.id in tictactoe:
            search = re.search("tictactoe ([0-9]):([0-9])", call.data)
            if search:
                move = int(search.group(1)) + int(search.group(2)) * 3
                if tictactoe[call.message.chat.id].valid(move):
                    result = tictactoe[call.message.chat.id].play2(move)
                    send_gamoku_info(call, result[0], 3, "tictactoe")
                    if result[1]:
                        message = translate(call.message.chat.id, "You won!") + " 😻"
                        if result[1] == 1:
                            message = translate(call.message.chat.id, "You lost!") + " 😈"
                        if result[1] == 3:
                            message = translate(call.message.chat.id, "It's a draw!") + " 😱"
                        send_end_game_info(call.message, message, "tictactoe")


@bot.callback_query_handler(func=lambda call: call.data.startswith("fiveinarow"))
def fiveinarow_start(call):
    if call.message:
        if call.data == "fiveinarow start":
            fiveinarow[call.message.chat.id] = Gomoku()
            board = fiveinarow[call.message.chat.id].state()
            # board = [[char.replace('X', '🔴').replace('O', '🔵') for char in row] for row in board]
            send_gamoku_info(call, board, 8, "fiveinarow")
        elif call.message.chat.id in fiveinarow:
            search = re.search("fiveinarow ([0-9]):([0-9])", call.data)
            if search:
                y, x = int(search.group(1)), 7 - int(search.group(2))
                if fiveinarow[call.message.chat.id].is_move_valid(x, y):
                    board, end_flag = fiveinarow[call.message.chat.id].play(x, y)
                    # board = [[char.replace('X', '🔴').replace('O', '🔵️') for char in row] for row in board]
                    send_gamoku_info(call, board, 8, "fiveinarow")
                    if end_flag:
                        message = translate(call.message.chat.id, "You won!") + " 😻"
                        if end_flag == 1:
                            message = translate(call.message.chat.id, "You lost!") + " 😈"
                        if end_flag == 3:
                            message = translate(call.message.chat.id, "It's a draw!") + " 😱"
                        send_end_game_info(call.message, message, "fiveinarow")


@bot.callback_query_handler(func=lambda call: call.data.startswith("matches"))
def matches_start(call):
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
                    (bot_move, end_flag) = matches[call.message.chat.id].play(new_state)
                    if end_flag:
                        send_end_game_info(call.message, translate(call.message.chat.id, "You lost!") + " 😈",
                                           "matches")
                    else:
                        send_matches_info(call, matches[call.message.chat.id].state, bot_move)


@bot.callback_query_handler(func=lambda call: call.data == "menu")
def menu(call):
    if call.message:
        main_menu(call.message)


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
        bot.send_message(call.message.chat.id, translate(call.message.chat.id, "Make your move!"), reply_markup=markup)
    else:
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=markup)


def send_matches_info(call, state, bot_move=0):
    global matches
    markup = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text=translate(call.message.chat.id, "Take one match"), callback_data="matches 1")]
    if state > 1:
        buttons.append(types.InlineKeyboardButton(text=translate(call.message.chat.id, "Take two matches"),
                                                  callback_data="matches 2"))
    if state > 2:
        buttons.append(types.InlineKeyboardButton(text=translate(call.message.chat.id, "Take three matches"),
                                                  callback_data="matches 3"))
    for button in buttons:
        markup.add(button)
    if call.data == "matches start":
        bot.send_message(call.message.chat.id,
                         translate(call.message.chat.id, "There are %d matches.\nMake your move!" % state),
                         reply_markup=markup)
    else:
        bot.edit_message_text(
            translate(call.message.chat.id,
                      "I took %d matches. There are %d matches left.\nMake your move!" % (bot_move, state)),
            call.message.chat.id,
            call.message.message_id, reply_markup=markup)


def send_end_game_info(message, text, game, btn1_text=None):
    if btn1_text is None:
        btn1_text = translate(message.chat.id, "Replay")
    reset_objects(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text=btn1_text, callback_data="%s start" % game),
               types.InlineKeyboardButton(text=translate(message.chat.id, "Menu"), callback_data="menu")]
    for button in buttons:
        markup.add(button)
    bot.send_message(message.chat.id, text, reply_markup=markup)


if __name__ == '__main__':
    while True:
        try:
            bot.polling(timeout=50, none_stop=True)
        except Exception as e:
            print("\n=============ERROR=============")
            print(e)
            print("=============ERROR=============\n")
            time.sleep(5)
            continue
        break