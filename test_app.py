from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            # DONE: check that correct HTML was returned
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- Test: this is the boggle homepage -->', html)
            # test that you're getting a template
            # DONE: select something specific, like a hidden "Test:" comment

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            response = client.post("/api/new-game")
            game_data = response.get_json() # <-- NOTE: this is not json. this is a dict

            # TODO: READY -
            # test that the response has attr "gameId"
            self.assertIn("gameId", game_data)
            # test that attr board is a list
            self.assertIsInstance(game_data["board"], list)
            # test that attr board contains only lists
            # TODO: NOTE: we could possibly use assertEqual(a,b) to see if game_data["board"] is equal to []
            self.assertFalse([False for row in game_data["board"] if not isinstance(row, list)])
            # test that games dictionary contains this gameId
            self.assertIn(game_data["gameId"], games)

    def test_api_score_word(self):
        """ Integration test for score route. Testing"""
        with self.client as client:
            new_game_response = client.post("/api/new-game")
            gameId = new_game_response.get_json()["gameId"]
        # NOTE: testing frameworks randomize order of tests - so you couldn't have relied on new game test
        #        Each test should stand alone
        # Change board letters
        # access the game by gameId, and change letters to be our okay word only
        boggle_game_instance = games[gameId]
        boggle_game_instance.board[0] = ["D", "O", "G", "X", "X"]

        # Okay test
        okay_word = "DOG"
        with self.client as client:
            score_word_response = client.post(
                "/api/score-word",
                json={"gameId": gameId, "wordInput":okay_word}
            )

            result = score_word_response.get_json() # this is the object of {result: _____}

            self.assertEqual(result, {"result":"ok"})

        # Not on board test
        not_on_board_word = "ALCOVES"
        with self.client as client:
            score_word_response = client.post(
                "/api/score-word",
                json={"gameId": gameId, "wordInput":not_on_board_word}
            )

            result = score_word_response.get_json() # this is the object of {result: _____}

            self.assertEqual(result, {"result":"not-on-board"})

        # Not a word test
        not_word = "Qalkdsjf"
        with self.client as client:
            score_word_response = client.post(
                "/api/score-word",
                json={"gameId": gameId, "wordInput":not_word}
            )

            result = score_word_response.get_json() # this is the object of {result: _____}

            self.assertEqual(result, {"result":"not-word"})