from flask import Flask, request, render_template, redirect, session, jsonify
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from dotenv import dotenv_values
from utilities import Database
import os

config = dotenv_values('.env')

# initialize Flask app
app = Flask(__name__)

# initialize CSRF protection
csrf = CSRFProtect(app)

app.secret_key = config['SECRET_KEY']

# initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)

# checks if working in local development environment or production environment
if 'CONNECTION_STRING' not in os.environ:
    # if connection string is not in local environment variables then we are working in local environment
    db = Database(config['LOCAL_DB'])

else:
    print('Loading production config')

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
    return render_template('index.html')

@app.route('/email_exists')
def email_exists():
    email = request.values.get('email')

    email_exists = db.email_exists(email)
    print(email_exists)
    return jsonify(result="complete")

if __name__ == '__main__':
    app.run()
