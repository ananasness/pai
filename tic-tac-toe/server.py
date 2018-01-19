from flask import Flask, request
from minmax_alg import MinMax
app = Flask(__name__)
TOKEN = "Bearer"
sessions = {}

@app.route("/")
def index():
    return "B4-SuperTicTacBot"

@app.route('/tictactoe/<int:session_id>/', methods=["POST"])
def tictactoe(session_id):
	if session_id not in sessions:
		sessions[session_id] = MinMax()
	if not request.headers.get("Authorization") == TOKEN:
		return "", 401

	try: 
		if request.get_data():
			move = int(request.get_data())
		else:
			move = -1
	except ValueError:
		return "", 403
	return "", sessions[session_id].play(move)
