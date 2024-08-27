from flask import Flask, request, render_template, redirect, session, jsonify
from flask_login import LoginManager
from dotenv import dotenv_values

config = dotenv_values('.env')

# initialize Flask app
app = Flask(__name__)

app.secret_key = config['SECRET_KEY']

# login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    user = None
    if user is not None:
        #if user.phone is Null:

        return user
    else:
        return None

@app.route('/')
def hello_world():  # put application's code here
    session['google_client'] = config['GOOGLE_LOGIN_CLIENTID']
    return render_template('layout.html')


if __name__ == '__main__':
    app.run()
