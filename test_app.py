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
            json = response.get_json() # <-- NOTE: this is not json. this is a dict

            # TODO: (DONE - Code review needed)
            # test that the response has attr "gameId"
            self.assertIn("gameId", json)
            # test that attr board is a list
            self.assertIsInstance(json["board"], list)
            # test that attr board contains only lists
            # NOTE: we could possibly use assertEqual(a,b) to see if json["board"] is equal to []
            self.assertFalse([False for row in json["board"] if not isinstance(row, list)])
            # test that games dictionary contains this gameId
            self.assertIn(json["gameId"], games)

