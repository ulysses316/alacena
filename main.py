from flask import Flask, url_for, render_template, redirect, session
from authlib.integrations.flask_client import OAuth
from credentials import c_id, c_secret

# Decorator for routes

from auth_decorator import login_required

app = Flask(__name__)
app.secret_key = 'Esta es mi super llave secreta'

# OAuth Config

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id= c_id,
    client_secret=c_secret,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope':'openid profile email'},
)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/products')
@login_required
def products():
    return render_template("products.html")

@app.route('/user')
@login_required
def user():
    profile = dict(session).get('profile',None)
    return render_template("user.html", profile=profile)



# Gooogle Login

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    # do something with the token and profile
    session['profile'] = user_info
    session.permanent = True
    return redirect('/products')

@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect("/")

# Errors

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404
