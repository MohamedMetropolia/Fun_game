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
    check_win_item int(2) DEFAULT 0,
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
       ("Feather"),
       ("Gold"),
       ("Sword"),
       ("Food Offerings"),
       ("Invisible Cloak"),
       ("Holy Chalice"),
       ("Shield"),
       ("Gemstone");

insert into location(description, location_text, map_image, encounter, encounter_text, encounter_image, use_item_decision, encounter_win_url, encounter_win_text, encounter_loose_url, encounter_loose_text, item, item_id, item_image, item_description, item_decision_text, direction_up, direction_down, direction_left, direction_right, check_win_item)
values ("Maze","You find yourself waking up in a maze. You have to find the exit in order to survive.","maze_map.png",0,"","","","","","","",0,0,"","","",3,0,4,2,0),
       ("Basement","You are walking downstairs to a cold and damp place with little to no light. It seems to be an old basement.","basement_map.png",0,"","","","","","","",1,4,"sword.png","Sword","Under a dusty blanket there seems to be a Sword. It might come in handy later on... Would you take it?",11,0,1,16,0),
       ("Crossroad","As you were moving you realize you''ve come to an intersection in the maze","crossroad_map.png",0,"","","","","","","",0,0,"","","",9,1,8,5,0),
       ("Graveyard","In the distance you see some slim silhouettes in the fog. As you walk closer, you realize that those are tombstones and you find yourself in the middle of a graveyard.","graveyard_map.png",1,"","","","","","","",0,0,"","","",0,0,17,1,0),
       ("Forest","You find yourself entering a forest","forest_map.png",0,"","","","","","","",0,0,"","","",10,6,3,7,0),
       ("Necropolis","You enter an extensive and elaborate burial place of an ancient city","necropolis_map.png",1,"","","","","","","",0,0,"","","",5,12,0,0,0),
       ("Fork","This path leads you outside to a fork","fork_map.png",0,"","","","","","","",0,0,"","","",0,0,0,0,0),
       ("Treasure Room","You find yourself walking into a treasure room!","treasureRoom_map.png",0,"","","","","","","",1,3,"gold.png","Gold","It is your lucky day, you have found some gold...Would you like to take it?",20,0,18,3,0),
       ("Cementery","You enter the cemetery causing the undead to become restless","cementery_map.png",1,"","","","","","","",0,0,"","","",22,3,0,0,0),
       ("Shed","You find yourself walking in a shed full of feathers!","shed_map.png",0,"","","","","","","",1,2,"feather.png","Feather","You find yourself walking in a shed full of feathers!...Would you take one?",23,5,0,0,0),
       ("Bandit Camp","You find yourself in the middle of a bandit camp, they don't look friendly","bandit_camp_map.png",1,"","","","","","","",0,0,"","","",0,2,0,12,0),
       ("Pond","You hear a splashing and see a pond up ahead, a mermaid greets you from the water","pond_map.png",1,"","","","","","","",0,0,"","","",6,16,11,13,0),
       ("Inn","The smell of food and the sound of laughter greets you as you find yourself at the inn.","inn_map.png",1,"","","","","","","",0,0,"","","",0,0,12,14,0),
       ("Shrine","A holy glow radiates from between the trees. A stone shrine is sitting in a clearing in the woods, surrounded by offerings.","shrine_map.png",1,"","","","","","","",1,5,"food.png","Food Offerings","",15,0,13,0,0),
       ("Scholar's Lair","A twirling tower looms above you. You see books, tomes and scrolls inside, and a strong arcane energy fills the air","lair_map.png",0,"","","","","","","",1,6,"cloak.png","Invisible Cloak","",0,14,7,0,0),
       ("Hut","A worn-down hut stands near the entrance to the forest. An old man is sitting on the porch, carving a wooden figure. From the looks of it, he is making a wooden wolf.","hut_map.png",1,"","","","","","","",0,0,"","","",12,0,2,0,0),
       ("Chapel","A sense of dread sits in your stomach as you approach the cold, stone walls of a chapel. The air inside is damp, and the very ground beneath your feet seems to hold its breath.","chapel_map.png",0,"","","","","","","",1,7,"chalice.png","Holy Chalice","",18,0,0,4,0),
       ("Cave","You approach an opening in the mountain which is covered in stalactites. It looks like a beast, baring its teeth at you.","cave_map.png",0,"","","","","","","",1,8,"shield.png","Shield","",19,17,0,8,0),
       ("Troll Hideout","A putrid smell hits your nose as you find yourself face-to-face with three hulking figures - trolls!","troll_hideout_map.png",1,"","","","","","","",0,0,"","","",0,18,0,20,0),
       ("Marsh","Your feet stick to the ground as you make your way through a marsh. A thick fog obscures your vision as you follow the near-invisible path. Despite the fog, you're certain something is watching you.","marsh_map.png",0,"","","","","","","",0,0,"","","",21,8,19,0,0),
       ("Broken Portal","A lone stone structure lies ahead of you, shattered and broken. The grass around it is burnt, and you find strange objects around it - items not from this world, you''re certain.","portal_map.png",0,"","","","","","","",1,9,"gemstone.png","Gemstone","",0,20,0,22,0),
       ("Bone Field","The stones under your feet turn lighter and lighter, until you realise they're not stones at all. The field ahead of you shines an ivory white, full of bones of various sizes and sources. What brought them here? You'd rather not think about it too much.","bone_field_map.png",0,"","","","","","","",0,0,"","","",0,9,21,23,0),
       ("Wolf","You hear pained whining coming from underneath a fallen tree a wolf has been trapped underneath! It's trying to free itself, but seems to be making no progress.","wolf_map.png",0,"","","","","","","",0,0,"","","",0,10,22,0,0),
       ("Demogorgon Room","You hear growling nearby","demogorgon_room_map.png",1,"You see a gigantic beast in front of you, showing its humongous fangs.","demogorgon.png","","","","","",0,0,"","","",0,0,0,0,0),
       ("Exit","Congratulations! you have find the exit.","exit.png",0,"","","","","","","",0,0,"","","",0,0,0,0,0);

insert into current_game(player, current_location, inventory, score)
values ("", 1, 1, 0)


