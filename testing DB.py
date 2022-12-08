from flask import Flask, jsonify, request, Blueprint, render_template, redirect, url_for, config
import json
import os
from flask_cors import CORS, cross_origin
import fun_game
import sys
import time
import random
import mysql.connector
import requests
import os
from os import system, name

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='fun_game',
    user='user0',
    password='',
    autocommit=True
)


def get_location_from_username(username):
    sql = "SELECT * " \
          "FROM location WHERE id in ( SELECT current_location FROM current_game WHERE player = '" + username + "') "
    # print(sql)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if cursor.rowcount > 0:
        for row in result:
            return row
    return
# def move_user_to_new_location(username, direction):


@app.route('/location/<username>')      # decorator
def location(username):
    a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u = get_location_from_username(username)
    response = {
        "player_name": username,
        "id": a,
        "location": b,
        "Location_description": c,
        "map_image": d,
        "encounter": e,
        "encounter_text": f,
        "encounter_image": g,
        "use_item_decision": h,
        "encounter_win_url": i,
        "encounter_win_text": j,
        "encounter_loose_url": k,
        "encounter_loose_text": l,
        "item": m,
        "item_id": n,
        "item_image": o,
        "item_description": p,
        "item_description_text": q,
        "direction_up": r,
        "direction_down": s,
        "direction_left": t,
        "direction_right": u
    }
    print(response)
    return response

location()

if __name__ == "__main__":
    app.run(debug=True)
