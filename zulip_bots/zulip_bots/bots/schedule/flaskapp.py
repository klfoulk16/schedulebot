import dotenv
import os
import flask

dotenv.load_dotenv()

app = flask.Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.run()
