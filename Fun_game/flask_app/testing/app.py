from flask import Flask, jsonify, request, Blueprint, render_template, redirect, url_for
import json
import os

import mysql.connector
from dotenv import load_dotenv
from flask_cors import CORS

import config
from fun_game import Main

app = Flask(__name__)

"""@app.route('/number/')
def print_list():
    return jsonify(list(range(5)))

@app.route('/person/')
def hello():
    return jsonify({"name": "Mido",
                    "address": "Finland",
                    "game": "fun_game",
                    "school": "Metropolia"})"""

@app.route("/")
def index():
    return render_template('home.html', login_fail=False)

@app.route('/game.html', methods=["POST", "GET"])
def gameplay():
    if request.method == "POST":
        output = request.get_json()
        print(output)
    return render_template('game.html')

@app.route('/gameover.html', methods=["POST", "GET"])
def restart():
    if request.method == "POST":
        output = request.get_json()
        print(output)
        jsonify(render_template("fun_game.py"))
    return render_template("gameover.html")

@app.route('/home.html', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        output = request.get_json()
        print(output)
    return render_template("home.html")

@app.route('/create_player/', methods=["POST"])
def create_player():
    player_name = new_player(name)


"""@app.route('/')
def run_script():
    file = open(r'fun_game.py', 'r').read()
    return exec(file)"""
"""
@app.route('/home/')
def home():
    return "Home page"

@app.route('/contact')
def contact():
    return "Contact page"

@app.route('/teapot/')
def teapot():
    return "Would you like some tea?", 418

@app.before_request
def before():
    print("This is executed before each request.")

@app.route('/hello/')
def hello():
    return "Hello world!"

app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(contact_bp, url_prefix='/contact')

app.logger.debug('This is a DEBUG message')
app.logger.info('This is an INFO message')
app.logger.warning('This is a WARNING message')
app.logger.error('This is an ERROR message')
"""
if __name__ == "__main__":
    app.run(debug=True)
