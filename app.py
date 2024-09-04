from flask import Flask, request, render_template, redirect, session, jsonify, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from dotenv import dotenv_values
from utilities import Database, gen_image, User
import base64
import os
import io
import base64

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
        return User(user)
    else:
        return None

@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/')

@app.route('/')
def home_page():  # put application's code here
    session['google_client'] = config['GOOGLE_LOGIN_CLIENTID']

    if current_user.is_authenticated:
        return redirect('/logged_in')
    else:
        return render_template('index.html')

@app.post('/login')
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember')

    remember = True if remember == "checked" else False
    dbUser = db.get_user_by_email(email)

    if dbUser is not None:
        if bcrypt.check_password_hash(dbUser[3], password):
            user = User(dbUser)
            login_user(user, remember=remember)

            return redirect('/logged_in')

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

    return redirect('/logged_in')

@app.route('/user_settings')
@login_required
def user_settings():
    return render_template('user_settings.html')

@app.route('/logged_in')
@login_required
def logged_in():
    return render_template('logged_in.html')

@app.post('/save_profile_pic')
@login_required
def save_profile_pic():
    """Updates user profile picture in database"""
    uploaded_pic = request.files['new_profile_pic'].read()
    #print(type(uploaded_pic.read()))
    data = io.BytesIO(uploaded_pic)

    encoded_img_data = base64.b64encode(data.getvalue())

    db.update_pic(current_user._id, encoded_img_data)
    return redirect(request.referrer)

@app.post('/save_theme')
@login_required
def save_theme():
    """Updates user profile theme in database"""
    theme = request.form.get('theme')
    db.update_theme(current_user._id, theme)

    return jsonify(data='success')

@app.post('/save_info')
@login_required
def save_info():
    name = request.form.get('name')
    email = request.form.get('email')

    db.update_info(current_user._id, name, email)

    return jsonify(data='success')

@app.post('/validate_pw')
@login_required
def validate_password():
    """Verifies the provided password matches the stored password"""
    password = request.form.get('old_password')

    if bcrypt.check_password_hash(current_user.password, password):
        result = True
    else:
        result = False

    return jsonify(result = result)

@app.post('/update_pw')
@login_required
def update_password():
    """Update password"""
    password = request.form.get('new_password')

    bc_password = bcrypt.generate_password_hash(password).decode('utf-8')

    db.update_password(current_user._id, bc_password)

    return jsonify(result = "complete")

if __name__ == '__main__':
    app.run()
