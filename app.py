from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    # DONE: add to the test to check that correct HTML was returned
    # NOTE: No game instantiation here: just table and script source, but isn't making game here
    # Don't want home page to make game b/c home page would be get request, get requests can be cached,
    #   cached game would be very bad
    # Best for home page to just be html and script source
    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    # DONE: add real id, real board, return JSON
    return jsonify({"gameId": game_id, "board": game.board})

@app.post('/api/score-word')
def is_legal_word():
    """Checks to see if word is in word list and on the board
       and returns JSON info re: word legality"""

    # TODO: READY - implement this route

    # QUESTION: docs for response methods? outside of dir(response)
    # ANSWER:   CHECK OUT FLASK API REPONSE

    # NOTE: accepts {'wordInput': 'WORD', 'gameId': gameId}
    response = request.json # <-- isn't json - it's a dict made by parsing json string
    # FIXME: Caution name of response, b/c we are making the response.  Better: input_data
    wordInput = response["wordInput"]
    gameId = response["gameId"]
    currentGame = games[f"{gameId}"] # FIXME:  already a string
    print(currentGame.__repr__())
    print("current game")

    # TODO: READY - check if wordInput is in word list and on board
    if (
        currentGame.word_list.check_word(wordInput) and # FIXME: change so okay is last. Often better to fail fast and have else be winning case
        currentGame.check_word_on_board(wordInput)
    ):
        word_legality = "ok"

    # TODO: READY - check if wordInput is not in word list
    elif not currentGame.word_list.check_word(wordInput):
        word_legality = "not-word"

    # TODO: READY - check if wordInput is not on board
    elif not currentGame.check_word_on_board(wordInput):
        word_legality = "not-on-board"

    return jsonify({"result": word_legality})

