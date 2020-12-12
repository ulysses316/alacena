from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/products')
def products():
    return render_template("products.html")


@app.route('/user')
def user():
    return render_template("user.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404