from flask import Flask, jsonify, request, Blueprint, render_template, redirect, url_for, config
import json
import os
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# mock data for JS testing
move_request_example = {
  "status": 200,
  "player_name": "John",
  "directions": ["left", "right", "up"],
  "location_id": 2,
  "location_name": "basement",
  "location_text": "You found yourself in a basement.",
  "map_image": "basement_map.png",
  "encounter": {
    "encounter_text": "You've found a Demogorgon in the room.if you happen to have a weapon you might find a way out",
    "encounter_image": "../img/demogorgon.png",
    "riddle_question": "riddle generator api text",
    "riddle_answer": "riddle generator api answer",
    "use_item_decision": "would you like to use the Sword?",
    "encounter_win_url": "/demogorgon/win",
    "encounter_win_text": "Congratulations! you have found a way out",
    "encounter_loose_url": "/death",
    "encounter_loose_text": "You cowardly decide to feed the beast with your flesh"
  },
  "item": {
    "id": 1,
    "image": "../img/sword.png",
    "description": "Sword"
  },
  "item_decision": {
    "item_decision_text": "Under a dusty blanket seems to be a Sword\nIt might come in handy later on...\n-->, would you take it?",
    "options": [
      {
        "button_text": "yes",
        "api_url": "/take/sword"
      },
      {
        "button_text": "no",
        "api_url": 0
      }
    ]
  }
}

"""@app.route('/number/')
def print_list():
    return jsonify(list(range(5)))

@app.route('/person/')
def hello():
    return jsonify({"name": "Mido",
                    "address": "Finland",
                    "game": "fun_game",
                    "school": "Metropolia"})"""


def success():
    return {
        "status": 200
    }


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
    # player_name = new_player(name)
    return success()  # this is mock api


@app.route('/death/', methods=["POST"])
def death():
    # read post data to check user
    # userName = request.form.get("username")
    # set user status to dead (in this case his location gets reset)
    return render_template("gameover.html")


@app.route('/move/<direction>', methods=["POST"])
def move(direction):
    # read post data to check user
    # userName = request.form.get("username")
    # get user location with username, using FunGame

    # check if moving direction is valid, using FunGame, you can skip this

    # load the new location into an object that can be returned as a JSON

    # return locationObject
    response = jsonify(move_request_example)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response  # this is mock api


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
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  response.headers.add('Access-Control-Allow-Credentials', 'true')
  return response

if __name__ == "__main__":
    app.run(debug=True)
