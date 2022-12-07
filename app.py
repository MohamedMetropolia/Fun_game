import logging

from flask import Flask, jsonify, request, Blueprint, render_template, redirect, url_for, config
import json
import os
from flask_cors import CORS, cross_origin
import fun_game

# we create the backend instance, use this to access functions in the fun_game
backend = fun_game.Main()

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# mock data for JS testing
basement_example = {
    "status": 200,
    "player_name": "John",
    "directions": ["left", "right", "up"],
    "location_id": 2,
    "location_name": "Basement",
    "location_text": "You are walking downstairs to a cold and damp place with little to no light. It seems to be an old basement.",
    "map_image": "basement_map.png",
    "encounter": {
        "encounter_text": "",
        "encounter_image": "",
        "riddle_question": "",
        "riddle_answer": "",
        "use_item_decision": "",
        "encounter_win_url": "",
        "encounter_win_text": "",
        "encounter_loose_url": "",
        "encounter_loose_text": ""
    },
    "item": {
        "id": 1,
        "image": "../img/sword.png",
        "description": "Sword"
    },
    "item_decision": {
        "item_decision_text": "Under a dusty blanket there seems to be a Sword. It might come in handy later on... Would you take it?",
        "options": [
            {
                "button_text": "yes",
                "api_url": "take/sword"
            },
            {
                "button_text": "no",
                "api_url": 0
            }
        ]
    }
}
start_location = {
    "status": 200,
    "player_name": "John",
    "directions": ["left", "right", "up"],
    "location_id": 1,
    "location_name": "Maze",
    "location_text": "You find yourself waking up in a maze. You have to find the exit in order to survive.",
    "map_image": "maze_map.png",
    "encounter": {
        "encounter_text": "",
        "encounter_image": "",
        "riddle_question": "",
        "riddle_answer": "",
        "use_item_decision": "",
        "encounter_win_url": "",
        "encounter_win_text": "",
        "encounter_loose_url": "",
        "encounter_loose_text": ""
    },
    "item": {
        "id": 0,
        "image": "",
        "description": ""
    },
    "item_decision": {
        "item_decision_text": "",
        "options": [
            {
                "button_text": "",
                "api_url": ""
            },
            {
                "button_text": "",
                "api_url": ""
            }
        ]
    }
}
graveyard_example = {
    "status": 200,
    "player_name": "John",
    "directions": ["left", "right"],
    "location_id": 4,
    "location_name": "Graveyard",
    "location_text": "In the distance you see slim sharp silhouettes in the fog. As you walk closer, you can see those are tombstones and you are in the middle of a graveyard.",
    "map_image": "graveyard_map.png",
    "encounter": {
        "encounter_text": "",
        "encounter_image": "",
        "riddle_question": "",
        "riddle_answer": "",
        "use_item_decision": "",
        "encounter_win_url": "",
        "encounter_win_text": "",
        "encounter_loose_url": "",
        "encounter_loose_text": ""
    },
    "item": {
        "id": 0,
        "image": "",
        "description": ""
    },
    "item_decision": {
        "item_decision_text": "",
        "options": [
            {
                "button_text": "",
                "api_url": ""
            },
            {
                "button_text": "",
                "api_url": ""
            }
        ]
    }
}


# helper functions that we need in flask
def success():
    return {
        "status": 200
    }
def fail():
    return {
        "status": 500
    }


def get_player_name_from_request():
    user_name = request.form.get("input_username")
    logging.info(request.form)
    if not user_name:
        user_name = request.cookies.get("input_username")
    return user_name


@app.route("/")
def index():
    return render_template('home.html', login_fail=False)


@app.route('/game.html', methods=["POST", "GET"])
def gameplay():
    player_name = get_player_name_from_request()
    response = app.make_response(render_template('game.html', input_username=player_name))
    return response


@app.route('/gameover.html', methods=["POST", "GET"])
def restart():
    return render_template("gameover.html")


@app.route('/home.html', methods=["POST", "GET"])
def home():
    if request.method == "POST":
        output = request.get_json()
        print(output)
    return render_template("home.html")


@app.route('/create_player', methods=["POST"])
def create_player():
    player_name = get_player_name_from_request()
    player_id = backend.new_player(player_name)
    #response = jsonify(player_data)
    response = app.make_response(render_template('game.html', input_username=player_name))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.set_cookie('input_username', player_name)
    return response


@app.route('/loot_item/<item>', methods=["POST"])
def loot_item(item):
    player_name = get_player_name_from_request()
    loot_data = backend.loot_item(player_name, item)
    response = jsonify({"status": 200})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/death/', methods=["POST"])
def death():
    player_name = get_player_name_from_request()
    # read post data to check user
    # userName = request.form.get("username")
    # set user status to dead (in this case his location gets reset)
    return render_template("gameover.html")


@app.route('/move/<direction>', methods=["POST"])
def move(direction):
    # read post data to check user
    player_name = get_player_name_from_request()

    # get user location with username, using FunGame and load the location into an object that can be returned as a JSON
    old_location = backend.get_location_from_username(player_name)
    # check if moving direction is valid, using FunGame, you can skip this
    if direction == "left":
        if old_location.get("direction_left"):
            new_location = backend.move_user_to_new_location(player_name, direction)
        else:
            return fail()
    if direction == "right":
        if old_location.get("direction_right"):
            new_location = backend.move_user_to_new_location(player_name, direction)
        else:
            return fail()
    if direction == "up":
        if old_location.get("direction_up"):
            new_location = backend.move_user_to_new_location(player_name, direction)
        else:
            return fail()
    if direction == "down":
        if old_location.get("direction_down"):
            new_location = backend.move_user_to_new_location(player_name, direction)
        else:
            return fail()
    # make location into a response JSON
    response = jsonify(new_location)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/current', methods=["POST"])
def current():
    # read post data to check user
    player_name = get_player_name_from_request()

    # get user location with username, using FunGame and load the location into an object that can be returned as a JSON
    old_location = backend.get_location_from_username(player_name)
    # check if moving direction is valid, using FunGame, you can skip this

    # make location into a response JSON
    response = jsonify(old_location)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response


if __name__ == "__main__":
    app.run(debug=True)
