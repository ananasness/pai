from flask import Flask, request
from minmax_alg import MinMax
import re
app = Flask(__name__)
TOKEN = "Bearer 1"
sessions = {}

@app.route("/")
def index():
    return "B4-SuperTicTacBot"

@app.route('/tictactoe/<int:session_id>', methods=["POST"])
def tictactoe(session_id):
	if not request.headers.get("Authorization") == TOKEN:
		return "", 401
	in_board = request.get_data().decode('utf-8')
	if session_id not in sessions:
		sessions[session_id] = MinMax()
	return sessions[session_id].play(in_board)
