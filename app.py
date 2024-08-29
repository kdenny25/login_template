from flask import Flask, request, render_template, redirect, session, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from dotenv import dotenv_values
from utilities import Database, gen_image, User
import base64
import os


config = dotenv_values('.env')

# initialize Flask app
app = Flask(__name__)

# initialize hashing method for user passwords
bcrypt = Bcrypt(app)

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
def load_user(userid):
    # after registration log user in
    user = db.get_user_by_id(userid)

    if user is not None:
        #if user.phone is Null:

        return User(user)
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/')

@app.route('/')
def home_page():  # put application's code here
    session['google_client'] = config['GOOGLE_LOGIN_CLIENTID']

    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    # log user out and redirect to home page
    logout_user()
    return redirect("/")

@app.route('/email_exists')
def email_exists():
    email = request.values.get('email')

    email_exists = db.email_exists(email)
    print(email_exists)
    return jsonify(result=email_exists)

@app.post('/register_user')
def register():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    image = gen_image(name)

    # encrypt password
    bc_password = bcrypt.generate_password_hash(password).decode('utf-8')

    db.register_user(name, email, bc_password, image)

    # after registration log user in
    user = User(db.get_user_by_email(email))

    login_user(user)

    return jsonify(result="Complete")

if __name__ == '__main__':
    app.run()
