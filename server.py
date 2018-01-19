from flask import Flask, request
app = Flask(__name__)
TOKEN = "Bearer"

@app.route("/")
def index():
    return "B4-SuperTicTacBot"

@app.route('/tictactoe/<int:session_id>/', methods=["POST"])
def tictactoe(session_id):
	if not request.headers.get("Authorization") == TOKEN:
		return "", 401
	return "nope"
	#return game(session_id, request.get_data())

