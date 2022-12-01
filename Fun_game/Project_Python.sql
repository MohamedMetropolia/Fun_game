#WRITTEN BY: Mohamed, Jeferson, Andrea, MD Shamiul

# Creating the database
DROP DATABASE IF EXISTS fun_game;
CREATE DATABASE fun_game;
USE fun_game;

# Creating the user so that they can instantly play the game.
create user 'user0'@'localhost' identified by '';
GRANT ALL PRIVILEGES ON fun_game.* TO 'user0'@'localhost';
flush privileges;

# Creating the tables.
CREATE TABLE items
(
    id          int(11) NOT NULL AUTO_INCREMENT,
    description varchar(40) DEFAULT NULL,
    PRIMARY KEY (id)
);
create table location
(
    id          int(11) NOT NULL AUTO_INCREMENT,
    description varchar(40) DEFAULT NULL,
    location_text varchar(255) DEFAULT '',
    map_image varchar(255) DEFAULT '',
    encounter int(2) DEFAULT 0,
    encounter_text varchar(255) DEFAULT '',
    encounter_image varchar(255) DEFAULT 'nyan.png',
    use_item_decision varchar(255) DEFAULT '',
    encounter_win_url varchar(255) DEFAULT '',
    encounter_win_text varchar(255) DEFAULT '',
    encounter_loose_url varchar(255) DEFAULT '',
    encounter_loose_text varchar(255) DEFAULT '',
    item int(2) DEFAULT 0,
    item_id int(40) DEFAULT 0,
    item_image varchar(255) DEFAULT '',
    item_description varchar(255) DEFAULT '',
    item_decision_text varchar(255) DEFAULT '',
    direction_up int(40) DEFAULT 0,
    direction_down int(40) DEFAULT 0,
    direction_left int(40) DEFAULT 0,
    direction_right int(40) DEFAULT 0,
    PRIMARY KEY (id)
);
create table current_game
(
     id               int(11) NOT NULL AUTO_INCREMENT,
     player           varchar(40) DEFAULT NULL,
     current_location int(40)     DEFAULT NULL,
     inventory        int(40) DEFAULT NULL,
     score            int(40) DEFAULT null,
     gold             int(40) DEFAULT null,
     gold_modifier    double default null,
     last_updated     timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    FOREIGN KEY (current_location) REFERENCES location (id),
    FOREIGN KEY (inventory) REFERENCES items(id)
);

create table visited_locations
(
     current_game_id     int(40) NOT NULL,
     location_id         int(40) NOT NULL,
     last_updated        timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (current_game_id,location_id),
    FOREIGN KEY (current_game_id) REFERENCES current_game(id),
    FOREIGN KEY (location_id) REFERENCES location(id)
);


# Adding the data to the tables
insert into items(description)
values ("Nothing"),
       ("feather"),
       ("Gold"),
       ("Sword");

insert into location(description, location_text, map_image, encounter, encounter_text, encounter_image, use_item_decision, encounter_win_url, encounter_win_text, encounter_loose_url, encounter_loose_text, item, item_id, item_image, item_description, item_decision_text, direction_up, direction_down, direction_left, direction_right)
values ("Maze","You find yourself waking up in a maze. You have to find the exit in order to survive.","maze_map.png",0,"","","","","","","",0,0,"","","",3,0,4,2),
       ("Basement","You are walking downstairs to a cold and damp place with little to no light. It seems to be an old basement.","basement_map.png",0,"","","","","","","",1,1,"sword.png","Sword","Under a dusty blanket there seems to be a Sword. It might come in handy later on... Would you take it?",11,0,1,16),
       ("Crossroad","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Graveyard","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Forest","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Necropolis","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Fork","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Treasure Room","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Cementery","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Shed","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Bandit Camp","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Pond","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Inn","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Shrine","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Scholar's Lair","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Hut","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Chapel","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Cave","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Troll Hideout","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Marsh","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Broken Portal","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Bone Field","","",0,"","","","","","","",0,0,"","","",0,0,0,0),
       ("Wolf","","",0,"","","","","","","",0,0,"","","",0,0,0,0);

insert into current_game(player, current_location, inventory, score)
values ("Starting player", 1, 1, 0)


