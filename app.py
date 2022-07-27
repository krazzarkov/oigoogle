from flask import Flask, flash, render_template, redirect, request, session
from flask.helpers import url_for
from flask_bootstrap import Bootstrap
from flask_login.utils import login_required, logout_user
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, current_user
from flask_login.mixins import UserMixin
from requests_oauthlib import OAuth2Session
import os

from wtforms import StringField, PasswordField
# from wtforms.validators import Length, Email
from werkzeug.security import generate_password_hash, check_password_hash
from dash_application import create_dash_application

# disable ssl requirement 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# discord authentication credentials 
base_discord_api_url = 'https://discordapp.com/api'
client_id = r'996586581009907723' # Get from https://discordapp.com/developers/apps
client_secret = '3m4wFqxR_QK1f_hzGGBfK9hNy5Txd0Gq'
# change the redirect uri to where you will be deploying the app+/oauth_callback 
redirect_uri='https://oicove.azurewebsites.net/oauth_callback'
scope = ['identify', 'email']
token_url = 'https://discordapp.com/api/oauth2/token'
authorize_url = 'https://discordapp.com/api/oauth2/authorize'

#start the flask app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)
# start the database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite.db"
Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager()
login.init_app(app)
create_dash_application(app)

# add admin and normal users 
# if the app is already running, add the users through the /register route
admin_users = ['Kraz#7145']
normal_users = ['fayezhesham#3805']

@login.user_loader
def user_loader(user_id):
    return User.query.filter_by(id=user_id).first()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(128), nullable=False)



class RegisterForm(FlaskForm):
    username = StringField("Username")
    role = StringField("Role")



for user in admin_users:
    check_user = User.query.filter_by(username = user).first()
    if not check_user:
        user = User(username= user, password=generate_password_hash('abc123'), role = "Admin")

        db.session.add(user)
        db.session.commit()




for user in normal_users:
    check_user = User.query.filter_by(username = user).first()
    if not check_user:
        user = User(username= user, password=generate_password_hash('abc123'), role = "User")
        
        db.session.add(user)
        db.session.commit()




@app.route("/")
def index():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)
    login_url, state = oauth.authorization_url(authorize_url)
    session['state'] = state

    return render_template("base.html", login_url = login_url)




@app.route("/oauth_callback")
def oauth_callback():
    discord = OAuth2Session(client_id, redirect_uri=redirect_uri, state=session['state'], scope=scope)
    token = discord.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.url,
    )
    session['discord_token'] = token
    return redirect(url_for('profile'))



@app.route("/profile")
def profile():
    discord = OAuth2Session(client_id, token=session['discord_token'])
    response = discord.get(base_discord_api_url + '/users/@me')
    if User.query.filter_by(username=response.json()['username'] + "#" + response.json()["discriminator"]).first():
        user = User.query.filter_by(username=response.json()['username'] + "#" + response.json()["discriminator"]).first()
        if check_password_hash(user.password, 'abc123'):
            login_user(user)
            return redirect(url_for('/dashboard/'))
    else:
        return render_template("not_authenticated.html")


@app.route("/register", methods=["GET", "POST"])
@login_required
def register():
    if not current_user.role == 'Admin':
        flash("You don't have access to this page", category = 'error')
        return redirect(url_for('index'))
    form = RegisterForm()

    if form.validate_on_submit() and form.role.data in ['Admin', 'User']:
        check_user = User.query.filter_by(username = form.username.data).first()
        if check_user:
            flash('User already exists.', category = 'error')
        else:
            user = User(username=form.username.data, password=generate_password_hash('abc123'), role = form.role.data)
            db.session.add(user)
            db.session.commit()
            flash('user added successfully', category = 'success')
        return render_template("register.html", form=form)
    else:
        flash('invalid role. valid roles are "Admin" and "User"', category = 'error')
    return render_template("register.html", form=form)



if __name__ == "__main__":
    app.run()