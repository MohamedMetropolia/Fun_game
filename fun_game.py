import sys
import mysql.connector
import requests

connection = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    database='fun_game',
    user='user0',
    password='',
    autocommit=True
)


# IDEA 1: a text based adventure game that allows the user to accept or decline items into his inventory.
# The inventory will be linked to mariaDB and called upon by the database driver in the code below.
# Coded by: Mohamed, Jeferson, Andrea, Immi.

# Line 472 has no return

# The game:
class Main:

    def __init__(self):
        pass

    def get_location_from_username(self, username):
        sql = "SELECT * FROM current_game WHERE player = %(username)s"
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(sql, {"username": username})
        result = cursor.fetchone()
        location = self.get_location_object_from_id(result.get("current_location"))
        location = self.add_user_stuff_to_location(location, username)
        return location
        # sql query to get the current_game from username(player name)
        # sql query to get location data for the current location of the player
        # return that location

    # function to move user to new direction
    def move_user_to_new_location(self, username, direction):
        old_location = self.get_location_from_username(username)
        # set user location to the location indicated in location_<direction>
        if direction == "up":
            self.set_location(username, old_location.get("direction_up"))
        if direction == "down":
            self.set_location(username, old_location.get("direction_down"))
        if direction == "left":
            self.set_location(username, old_location.get("direction_left"))
        if direction == "right":
            self.set_location(username, old_location.get("direction_right"))
        new_location = self.get_location_from_username(username)
        # return that location
        return new_location

    # function gets location object from DB data. With this function you no longer need the other hardcoded location
    # functions, and you all can add new locations easily to the DB
    def get_location_object_from_id(self, location_id):
        # sql query to get location data from location_id
        sql = "SELECT * FROM location WHERE id=%(location_id)s"
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(sql, {"location_id": location_id})
        data = cursor.fetchone()
        directions = []
        if data.get("direction_up"):
            directions.append("up")
        if data.get("direction_down"):
            directions.append("down")
        if data.get("direction_left"):
            directions.append("left")
        if data.get("direction_right"):
            directions.append("right")
        # add data to the object
        if data.get("riddle"):
            riddle = self.riddle()
            riddle_question = riddle.get("question")
            riddle_answer = riddle.get("answer")
        else:
            riddle_question = ""
            riddle_answer = ""
        if data.get("encounter"):
            encounter = {
                "encounter_text": data.get("encounter_text"),
                "encounter_image": data.get("encounter_image"),
                "riddle_question": riddle_question,
                "riddle_answer": riddle_answer,
                "use_item_decision": data.get("item_decision_text"),
                "encounter_win_url": data.get("encounter_win_url"),
                "encounter_win_text": data.get("encounter_win_text"),
                "encounter_loose_url": data.get("encounter_loose_url"),
                "encounter_loose_text": data.get("encounter_loose_text")
            }
        else:
            encounter = {"encounter_text": 0}

        if data.get("item"):
            item_decision = {
                "item_id": data.get("item_id"),
                "item_image": data.get("item_image"),
                "item_description": data.get("item_description"),
                "item_decision_text": data.get("item_decision_text")
            }
        else:
            item_decision = {"item_id": 0}
        location = {
            "status": 200,
            "player_name": "",
            "directions": directions,
            "location_id": data.get("id"),
            "direction_left": data.get("direction_left"),
            "direction_right": data.get("direction_right"),
            "direction_up": data.get("direction_up"),
            "direction_down": data.get("direction_down"),
            "location_name": data.get("description"),
            "location_text": data.get("location_text"),
            "map_image": data.get("map_image"),
            "encounter": encounter,
            "item": {},
            "item_decision": item_decision
        }
        # return that location
        return location

    # Function to add riddles
    def riddle(self):
        riddle = "https://riddles-api.vercel.app/random"
        response = requests.get(riddle).json()
        question = response.get('riddle')
        correct = response.get('answer')
        riddle = {
            "question": question,
            "answer": correct
        }
        return riddle

    def new_player(self, player_name):
        # this is a check if the player exists
        sql = "SELECT player FROM current_game WHERE player=%(player_name)s"
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(sql, {"player_name": player_name})
        if cursor.rowcount == 0:
            sql = "INSERT INTO current_game (player, current_location) VALUE (%(player_name)s,1)"
            cursor = connection.cursor(dictionary=True, buffered=True)
            cursor.execute(sql, {"player_name": player_name})
            user_id = cursor.lastrowid
            self.add_visited_location(user_id, 1)
        return

    def loot_item(self, player_name, item):
        sql = "UPDATE current_game SET inventory=%(item)s WHERE player=%(player_name)s"
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(sql, {"player_name": player_name, "item": item})
        return cursor.lastrowid

    def add_user_stuff_to_location(self, location, username):
        sql = "SELECT * FROM current_game WHERE player=%(username)s"
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(sql, {"username": username})
        result = cursor.fetchone()
        if result.get("inventory"):
            item = self.get_item_by_id(result.get("inventory"))
        else:
            item = {
                "id": 0,
                "image": "",
                "description": ""
            }
        location["item"] = item
        location["player_name"] = username
        location["map_image"] = self.generate_map(username)
        return location

    def get_item_by_id(self, item_id):
        sql = "SELECT * FROM items WHERE id=%(id)s"
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(sql, {"id": item_id})
        result = cursor.fetchone()

        item = {
            "id": item_id,
            "image": result.get("id"),  # todo: this should be item image url
            "description": result.get("description")
        }
        return item

    def generate_map(self, username):
        user_id = self.get_user_id(username)
        sql = "SELECT current_game_id, location_id FROM visited_locations WHERE current_game_id=%(user_id)s"
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(sql, {"user_id": user_id})
        result = cursor.fetchall()
        map_image_list = []
        if cursor.rowcount > 0:
            for row in result:
                location = self.get_location_object_from_id(row["location_id"])
                map_url = location.get("map_image")
                map_image_list.append(map_url)
        return map_image_list

    def get_user_id(self, username):
        sql = "SELECT * FROM current_game WHERE player=%(username)s"
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(sql, {"username": username})
        result = cursor.fetchone()
        return result.get("id")

    def set_location(self, username, location_id):
        sql = "UPDATE current_game SET current_location=%(location_id)s WHERE player=%(username)s"
        cursor = connection.cursor(dictionary=True, buffered=True)
        cursor.execute(sql, {"username": username, "location_id": location_id})
        self.add_visited_location(self.get_user_id(username), location_id)

    def add_visited_location(self, user_id, location_id):
        try:
            # this is a check if the player visited the location
            sql = "SELECT * FROM visited_locations WHERE current_game_id=%(current_game_id)s AND location_id=%(location_id)s"
            cursor = connection.cursor(dictionary=True, buffered=True)
            cursor.execute(sql, {"current_game_id": user_id, "location_id": location_id})
            if cursor.rowcount == 0:
                sql = "INSERT INTO visited_locations (current_game_id, location_id) VALUE (%(user_id)s,%(location_id)s)"
                cursor = connection.cursor(dictionary=True, buffered=True)
                cursor.execute(sql, {"user_id": user_id, "location_id": location_id})
        except mysql.connector.errors.IntegrityError as e:
            raise

