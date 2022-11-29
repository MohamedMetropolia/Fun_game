import sys
import time
import random
import mysql.connector
import os
from os import system, name

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

# The game:
def start_game(self):
    pass


class main:
    def __init__(self):
        None

    def start_game(self):
        # Code block that prints an updating line indicating that the game is loading up.
        a = 0
        for x in range(0, 3):
            a = a + 1
            b = ("Loading" + "." * a)
            sys.stdout.write('\r' + b)
            sys.stdout.flush()
            time.sleep(0.3)
        print(a,  end="\r")

    # function that simulates real typing for easier reading
        def print_slow(str):
            for text in str + '\n':
                sys.stdout.write(text)
                sys.stdout.flush()
                time.sleep(0)  # change to 0.01 after testing or 0.0 during testing

    # function that clears text
        def clear():
            print("\n" * 100)

    # function that allows the user to choose whether to replay the game or quit after death.
        def death():
            print_slow("You have died. Do you want to replay the game from the beginning?")
            print("Type 1 to reload\n""Type 2 to quit ")
            choice = input("--> ")
            if choice == "1":
                clear()
                start_game(self)
            elif choice == "2":
                print("Goodbye!")
                sys.exit()

    # function that allows the user to choose whether to replay the game or quit
        def replay():
            print_slow("Do you want to replay the game from the beginning?")
            print("Type 1 to reload\n""Type 2 to quit ")
            choice = input("--> ")
            if choice == "1":
                clear()
                start_game(self)
            elif choice == "2":
                print("Goodbye!")
                sys.exit()

    # Function that lets the user know where they are.
        def whereami():
            sql = "SELECT description FROM location WHERE id in ( SELECT current_location FROM current_game WHERE id = 1 )"
            # print(sql)
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            if cursor.rowcount > 0:
                for row in result:
                    print(f"Current location is: {row[0]}")

    # Function to update the player's current location.
        location = 1
        def current_location(location):
            sql = "UPDATE current_game SET current_location = '{}'".format(location)
            # print(sql)
            cursor = connection.cursor()
            cursor.execute(sql)
        current_location(location)

    # Function to update the player's inventory.
        item = 1
        def inventory(item):
            sql = "UPDATE current_game SET inventory = '{}'".format(item)
            # print(sql)
            cursor = connection.cursor()
            cursor.execute(sql)
        inventory(item)

    # Function to check the inventory
        def check_inventory():
            sql = "SELECT description FROM items WHERE id in ( SELECT inventory FROM current_game WHERE id = 1 )"
            # print(sql)
            cursor = connection.cursor()
            cursor.execute(sql)
            result = cursor.fetchall()
            if cursor.rowcount > 0:
                for row in result:
                    value = row[0]
            return value

    # Function to add a score feature
        """
        def score():
            gold = 0
            gold = gold + 50
            sql = "UPDATE current_game SET score += 50"
            sql += "WHERE id = 1"
            cursor = connection.cursor()
            cursor.execute(sql)
            print(gold)
            score()
        """

    # The introduction of the game
        print_slow("Welcome to our text based adventure game! (now officially supporting mariadb)")
        print_slow("We know that you're all too eager to start playing but first, let us know your name")
        name = input("--> So, what is your name? ")
        check = input(f"--> it appears that your name is {name}, is that correct? ")
    # Basic check to make sure the player has the name they want.
        if check == "NO".lower():
            print_slow("Uhm, alright. Let's try that again.")
            name = input("--> So, what is your name? ")
        print_slow(f"Alrighty {name}, it is a pleasure to meet you!")
        print("\n")

    # Adding the name variable into the database
        def new_player(name):
            sql = "UPDATE current_game SET player = '{}'".format(name)
            # print(sql)
            cursor = connection.cursor()
            cursor.execute(sql)
        new_player(name)

    # Here we will be explaining how the game is supposed to be played.
        def intro():
            print_slow(f"{name}, as your lovely host, it is my utmost "
                       f"pleasure to explain to you how this game is supposed to be played.")
            print_slow("With that being said, let me go ahead and read the instructions now. ")
            print_slow("Type UP, BACK, LEFT or RIGHT to move to different rooms")
            print_slow("incase you find items you are able to accept or decline them into your inventory.")
            print_slow("You can only carry ONE item at a time.")
            print_slow("The wrong choices might lead to certain death...")
            print_slow("CERTAIN DEATH?? Oh right, I'm not the one dying. ")
            print_slow(f"Welp, there you have it and best of luck {name}!")
            print("\n")
        intro()

    # Here will be the functional part where the user can play the game.
        print_slow("You find yourself waking up in a maze. You have to find the exit in order to survive.")
        def maze():
            location = 1  # Maze
            current_location(location)
            whereami()
            directions = ["left", "right", "up"]
            print_slow("Choose a direction among left, right or up to move  ")
            print_slow(f"Your current inventory is: {check_inventory()}")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print_slow("Sorry, here your options are left, right or up")
                direction = input("--> Which direction would you like to go? ").lower()
            if direction in directions:
                if direction == "left":
                    print("You decided on walking left")
                    print("\n")
                    graveyard()
                elif direction == "right":
                    print("You decided on walking right")
                    print("\n")
                    basement()
                elif direction == "up":
                    print("You decided on walking up")
                    print("\n")
                    crossroad()

    # Room where we could introduce the inventory mechanics(sql) to the player.
        def basement():     # Changed name
            location = 2    # basement
            current_location(location)
            whereami()
            directions = ["left", "right", "up"]
            print_slow("You find yourself walking downstairs to the basement!") # Needs elaboration
            # Condition to check wether the user already has this item
            print_slow("Under a dusty blanket seems to be a Sword")
            print_slow("It might come in handy later on...")
            print("""
                     /\´
                    /  |
      *            /  /________________________________________________
     (O)77777777777)  7                                                `~~--__
    8OO>>>>>>>>>>>>] <===========================================>          __-
     (O)LLLLLLLLLLL)  L________________________________________________.--~~
      *            \   |
                    \  |
                     \/
            """)
            decision = input("-->, would you take it? y/n: ").lower()
            if decision == "y":
                item = 4
                inventory(item)
                print("Now you have a Sword in your inventory")
                print("\n")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print("sorry, here you can only go left, right, up")
                direction = input("--> Which direction would you like to go? ")
            if direction in directions:
                if direction == "left":
                    print("You decided on walking left")
                    print("\n")
                    maze()
                elif direction == "right":
                    print("You decided on walking right")
                    print("\n")
                    # New room
                elif direction == "up":
                    print("You decided on walking up")
                    print("\n")
                    # New room

        def crossroad():
            location = 3  # Crossroad
            current_location(location)
            whereami()
            directions = ["left", "right", "up", "down"]
            print_slow("As you were moving you realize you've come to an intersection in the maze")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print_slow("sorry, here your options are left, right, up or down")
                direction = input("--> Which direction would you like to go? ").lower()
            if direction in directions:
                if direction == "left":
                    print("You decided on walking left")
                    print("\n")
                    treasure_room()
                elif direction == "right":
                    print("You decided on walking right")
                    print("\n")
                    forest()
                elif direction == "up":
                    print("You decided on walking forward")
                    print("\n")
                    cemetery()
                elif direction == "down":
                    print("You decided on walking down")
                    print("\n")
                    maze()

        # Possibly introducing the player to combat mechanics and death.
        def graveyard():
            location = 4  # Graveyard
            current_location(location)
            whereami()
            directions = ["up", "right", "left"]
            print_slow("This path leads you outside to a graveyard")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print("Sorry, here you can only go up, left or right")
                direction = input("--> Which direction would you like to go? ")
            if direction in directions:
                if direction == "up":
                    # Include questions or encounter before death
                    print_slow("You've fallen to your death...END")
                    time.sleep(2)
                    death()
                elif direction == "right":
                    print("You decided to go right")
                    print("\n")
                    maze()
                elif direction == "left":
                    print("You decided to go left")
                    print("\n")
                    # New room

        def forest():
            location = 5
            current_location(location)
            whereami()
            directions = ["left", "right", "up", "down"]
            print_slow("You find yourself entering a forest")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print_slow("Your options here are left, right, up or down")
                direction = input("--> Which direction would you like to go? ")
            if direction in directions:
                if direction == "left":
                    print("You decided on walking left")
                    print("\n")
                    crossroad()
                elif direction == "right":
                    print("You decided on walking right")
                    print("\n")
                    fork()
                elif direction == "up":
                    print("You decided on walking up")
                    print("\n")
                    shed()
                elif direction == "down":
                    print("You decided on walking down")
                    print("\n")
                    necropolis()

        def necropolis():
            location = 6
            current_location(location)
            whereami()
            directions = ["down", "left", "up"]
            print_slow("The left path leads outside to Necropolis")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print("Sorry, here you can only go down, left or up")
                direction = input("--> Which direction would you like to go? ").lower()
            if direction in directions:
                if direction == "left":
                    # Include questions or encounter before death
                    print_slow("As you tried moving to the left a horde of undead dogs attacked you...END")
                    print("""
                                 __
                        \ ______/ V`-,
                        }        /~~
                        /_)^ --,r'
                       |b      |b
                    """)
                    time.sleep(1)
                    print("""
                                        .-^^^^^^-.
        `;-,                           /     @) @)\´
          \-\                         |            `-.
           \=\    _oO)\O)\O)\O)\Oo_OOo=\         _    \´
            \-\oO( )/ // // // /_(_` )~`\        @)   /
             ( ` )|/ // // // /( ` )|    `-.__     _.'
             || |||| || || || | | | |         VvvvvV
             \| |||| || || || | | | |
              | ||)| || || || | | | _)
             (_,_))\ \´\ \´\_;`-'(_,_) )
             ( ' )\ `-'`-'     ( ` ) \´
              | |\ \            `\ \´\ \´
              | | \ \             \ \´\ \.
              | | (_,_)            \ \. _)
             (_,_)\)\)\)           (_,_)\)
             \)\)\)' ' '           \)\)\)'
              ' ' '                 ' ' '
    
                    """)
                    time.sleep(1)
                    print(""" 
                        .--~~,__
            :-....,-------`~~'._.'
            `-,,,  ,_      ;'~U'
            _,-' ,'`-__; '--.
            (_/'~~      ''''(;
                    """)
                    time.sleep(2)
                    death()
                elif direction == "up":
                    print("You've walked up")
                    print("\n")
                    forest()
                elif direction == "down":
                    print("You've walked up")
                    print("\n")
                    # New room

        def fork():
            location = 7
            current_location(location)
            whereami()
            directions = ["right", "left", "up", "down"]
            print_slow("This path leads you outside to a fork")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print("Sorry, here you can only go up, down, right or left")
                direction = input("--> Which direction would you like to go? ").lower()
            if direction in directions:
                if direction == "up":
                    print_slow("You've found a Demogorgon in the room")
                    print_slow("if you happen to have a weapon you might find a way out")
                    print("""                            ,-.                               
           ___,---.__          /'|`\          __,---,___          
        ,-'    \`    `-.____,-'  |  `-.____,-'    //    `-.       
      ,'        |           ~'\     /`~           |        `.      
     /      ___//              `. ,'          ,  , \___      \    
    |    ,-'   `-.__   _         |        ,    __,-'   `-.    |    
    |   /          /\_  `   .    |    ,      _/\          \   |   
    \  |           \ \`-.___ \   |   / ___,-'/ /           |  /  
     \  \           | `._   `\´\  |  //'   _,' |           /  /      
      `-.\         /'  _ `---'' , . ``---' _  `\         /,-'     
         ``       /     \    ,='/ \`=.    /     \       ''          
                 |__   /|\_,--.,-.--,--._/|\   __|                  
                 /  `./  \´\`\ |  |  | /,//' \,'  \                  
                /   /     ||--+--|--+-/-|     \   \                 
               |   |     /'\_\_\ | /_/_/`\     |   |                
                \   \__, \_     `~'     _/ .__/   /            
                 `-._,-'   `-._______,-'   `-._,-'""")
                    if check_inventory() == "Sword":
                        user_decision = input(f"would you like to use the {check_inventory()}? y/n ").lower()
                        if user_decision == "y":
                            print_slow(f"You fight your way out with the {check_inventory()} and drag yourself out of the room")
                            print("congratulations! you have found a way out")
                            print_slow(f"you finish the game with a {check_inventory()}")
                            replay()
                        elif user_decision == "n":
                            print("You cowardly decide to feed the beast with your flesh")
                            time.sleep(2)
                            death()
                    elif check_inventory() == "feather":
                        user_decision = input(f"would you like to use the {check_inventory()}? y/n ").lower()
                        if user_decision == "y":
                            print_slow(f"You tried unsuccessfully to tickle the beast with your {check_inventory()}")
                            print_slow("but it just ended up bad for you")
                            print_slow("The beast looks at you as if it was judging your choices before eating you out of pity...END")
                            time.sleep(2)
                            death()
                        elif user_decision == "n":
                            print("You cowardly decide to feed the beast with your flesh")
                            time.sleep(2)
                            death()
                    else:
                        print_slow("Empty handed there is nothing you can do against the beast...")
                        print_slow("You've become the beast's chew toy...END")
                        time.sleep(2)
                        death()
                    # Need some piece of code that check in the DB if the user have certain item
                elif direction == "down":
                    if check_inventory() == "Gold":
                        print_slow(f"You were able to sell off the gold you found for an extra 1000 points!")
                    print("congratulations! you have found a way out!")
                    print_slow(f"you finish the game with {check_inventory()}")
                    # SQL code SELECT the items that were collected along the game and show them to the user
                    replay()
                elif direction == "left":
                    print("You decided on walking left")
                    print("\n")
                    forest()
                elif direction == "right":
                    print("You decided on walking right")
                    print("\n")
                    # New Room

        def treasure_room():    # new added function
            location = 8    # treasure_room
            current_location(location)
            whereami()
            directions = ["up", "right", "left"]
            print_slow("You find yourself walking into a treasure room!")
            # Condition to check wether the user already has this item
            print_slow("It is your lucky day, you have found some gold")
            decision = input("-->, would you like to take it? y/n: ").lower()
            if decision == "y":
                item = 3
                inventory(item)
                print_slow("Now you have 50 gold")
            # Here we need to add statement of item No. 2 ("Gold")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print_slow("You can only go up, right or left from here")
                direction = input("--> Which direction would you like to go? ").lower()
            if direction in directions:
                if direction == "left":
                    print("You decided on walking left")
                    print("\n")
                    # New Room
                elif direction == "right":
                    print("You decided on walking right")
                    print("\n")
                    crossroad()
                elif direction == "up":
                    print("You decided on walking up")
                    print("\n")
                    # New Room

        def cemetery():     # new added function
            location = 9  # cemetery
            current_location(location)
            whereami()
            directions = ["up", "down", "right"]
            print_slow("Going forwards leads you into a cemetery")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print_slow("Sorry, here you can only go to the up or down")
                direction = input("--> Which direction would you like to go? ").lower()
            if direction in directions:
                if direction == "right":
                    print_slow("A flying skull hit you on the head...END")
                    print("""                                                  _________-----_____
                                                                    _____------           __      ----_
                                                             ___----             ___------              \`
                                                                ----________        ----                 \`
                                                                            -----__    |             _____)
                                                                                 __-                /     \`
                                                                     _______-----    ___--          \    /)\`
                                                               ------_______      ---____            \__/  /
                                                                          -----__    \ --    _          /\`
                                                                                 --__--__     \_____/   \_/\`
                                                                                         ----|   /          |
                                                                                             |  |___________|
                                                                                             |  | ((_(_)| )_)
                                                                                             |  \_((_(_)|/(_)
                                                                                             \             (
                                                                                             \_____________)""")
                    time.sleep(1)
                    print("""                                  _________-----_____
                                                    _____------           __      ----_
                                             ___----             ___------              \`
                                                ----________        ----                 \`
                                                            -----__    |             _____)
                                                                 __-                /     \`
                                                     _______-----    ___--          \    /)\`
                                               ------_______      ---____            \__/  /
                                                          -----__    \ --    _          /\`
                                                                 --__--__     \_____/   \_/\`
                                                                         ----|   /          |
                                                                             |  |___________|
                                                                             |  | ((_(_)| )_)
                                                                             |  \_((_(_)|/(_)
                                                                             \             (
                                                                             \_____________)""")
                    time.sleep(1)
                    print("""                  _________-----_____
                                    _____------           __      ----_
                             ___----             ___------              \`
                                ----________        ----                 \`
                                            -----__    |             _____)
                                                 __-                /     \`
                                     _______-----    ___--          \    /)\`
                               ------_______      ---____            \__/  /
                                          -----__    \ --    _          /\`
                                                 --__--__     \_____/   \_/\`
                                                         ----|   /          |
                                                             |  |___________|
                                                             |  | ((_(_)| )_)
                                                             |  \_((_(_)|/(_)
                                                             \             (
                                                             \_____________)""")
                    time.sleep(2)
                    death()
                    # Adding the option  if the player wants to play again
                    start_game(self)
                elif direction == "down":
                    print("You've walked back")
                    print("\n")
                    crossroad()
                elif direction == "up":
                    print("You've walked up")
                    print("\n")
                    # New Room

        def shed():         # new added function
            location = 10    # shed
            current_location(location)
            whereami()
            directions = ["up", "down"]
            print_slow("You find yourself walking in a shed full of feathers!")
            # Condition to check wether the user already has this item
            print("""
            
        (`/\´      (`/\´            (`/\´      (`/\´
        `=\/\´     `=\/\´           `=\/\´     `=\/\´
         `=\/\´     `=\/\´           `=\/\´     `=\/\´
          `=\/       `=\/             `=\/       `=\/
             \´         \´               \´         \´
            """)
            decision = input("-->, would you like to take one? y/n: ").lower()
            if decision == "y":
                item = 2
                inventory(item)
                print_slow("Now you got a feather")
            # Here we need to add statement of item No. 2 ("Feather")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print_slow("You can only go back from here")
                direction = input("--> Which direction would you like to go? ").lower()
            if direction in directions:
                if direction == "up":
                    print("You decided on walking up")
                    print("\n")
                    # New Room
                elif direction == "down":
                    print("You decided on walking down")
                    print("\n")
                    forest()
        maze()
    start_game(None)


    """    
    Template for the new rooms
    def NewRoom():
            location = 3   # Crossroad
            current_location(location)
            whereami()
            directions = ["left", "right", "up", "down"]
            print_slow("Piece of text that explain where is the USER")
            direction = input("--> Which direction would you like to go? ").lower()
            while direction not in directions:
                print_slow("sorry, here your options are left, right, up or down")
                direction = input("--> Which direction would you like to go? ").lower()
            if direction in directions:
                if direction == "left":
                    print("You decided on walking left")
                    print("\n")
                    # Next Room ()
                elif direction == "right":
                    print("You decided on walking right")
                    print("\n")
                    # Next Room ()
                elif direction == "up":
                    print("You decided on walking up")
                    print("\n")
                    # Next Room ()
                elif direction == "down":
                    print("You decided on walking down")
                    print("\n")
                    # Next Room ()
    """
