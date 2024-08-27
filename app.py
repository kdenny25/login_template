from flask import Flask, request, render_template, redirect, session, jsonify
from flask_login import LoginManager
from dotenv import load_dotenv

config = load_dotenv('.env')

# initialize Flask app
app = Flask(__name__)

# login manager
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('layout.html')


if __name__ == '__main__':
    app.run()
