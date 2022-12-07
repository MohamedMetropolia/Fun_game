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
    riddle int(2) DEFAULT 0,
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
       ("Diamond"),
       ("Sword"),
       ("Invisible Cloak"),
       ("Holy Chalice"),
       ("Shield");

insert into location(description, location_text, map_image, encounter, encounter_text, encounter_image, use_item_decision, encounter_win_url, encounter_win_text, encounter_loose_url, encounter_loose_text, item, item_id, item_image, item_description, item_decision_text, direction_up, direction_down, direction_left, direction_right, check_win_item, riddle)
values ("Maze","You find yourself waking up in a maze. You have to find the exit in order to survive.","maze_map.png",0,"","","","","","","",0,0,"","","",3,0,4,2,0,0),
       ("Basement","You are walking downstairs to a cold and damp place with little to no light. It seems to be an old basement.","basement_map.png",0,"","","","","","","",1,4,"sword.png","Sword","Under a dusty blanket there seems to be a Sword. It might come in handy later on... Would you take it?",11,0,1,16,0,0),
       ("Crossroad","As you were moving you realize you''ve come to an intersection in the maze","crossroad_map.png",0,"","","","","","","",0,0,"","","",9,1,8,5,0,0),
       ("Graveyard","In the distance you see some slim silhouettes in the fog. As you walk closer, you realize that those are tombstones and you find yourself in the middle of a graveyard.","graveyard_map.png",0,"","","","","","","",0,0,"","","",0,0,17,1,0,0),
       ("Forest","You find yourself entering a forest","forest_map.png",0,"","","","","","","",0,0,"","","",10,6,3,7,0,0),
       ("Necropolis","You enter an extensive and elaborate burial place of an ancient city","necropolis_map.png",1,"An horde of undead dogs attack you","undeadDogs.png","Would you like to use your item?","","You sent the dogs back to their grave","","You get moulled by the dogs and you join them in their graves...END...",0,0,"","","",5,12,0,0,4,0),
       ("Fork","This path leads you outside to a fork","fork_map.png",0,"","","","","","","",0,0,"","","",0,0,0,0,0,0),
       ("Treasure Room","You find yourself walking into a treasure room!","treasureRoom_map.png",1,"It is your lucky day, you have found a diamond...Would you like to take it?","diamond.png","","","","","",1,3,"","","",20,0,18,3,0,0),
       ("Cementery","You enter the cemetery causing the undead to become restless","cementery_map.png",1,"You see ere glowing behind old graves, suddenly you see  flying skulls towards you","skulls.png","Would you like to use your item?","","The chalice glow brigther than the skulls and the skulls fall down to the ground and shatter no longer glowing.","","The skulls drag your soul to hell.",0,0,"","","",22,3,0,0,6,0),
       ("Shed","You find yourself walking in a shed full of feathers!","shed_map.png",0,"","","","","","","",1,2,"feather.png","Feather","You find yourself walking in a shed full of feathers!...Would you take one?",23,5,0,0,0,0),
       ("Bandit Camp","You find yourself in the middle of a bandit camp, they don't look friendly","banditCamp_map.png",1,"A bandit approaches you drawing his sword","bandit.png","Would you like to use your item?","","You take the bandit by surprise and push him to the ground, he seems to be too scare to get up","","The armed bandit moves too fast for you to react - the last thing you see is the blade, directed at you.",0,0,"","","",0,2,0,12,4,0),
       ("Pond","You hear a splashing and see a pond up ahead.","pond_map.png",1,"A mermaid greets you from the water! She invites you closer and asks you a riddle.","mermaid.png","","","The mermaid looks happy with your answer as she splashes with her fins, she gives you some gold for it","","She suddenly has a angry expresion on her face. She jumps back into the water and swims away",0,0,"","","",6,16,11,13,0,1),
       ("Inn","The smell of food and the sound of laughter greets you as you find yourself at the inn.","inn_map.png",1,"A knight that has had too much drinks approaches, looks like he is in the mood to throw a punch.","knight.png","","","Despite his state, the knight decides against fighting a sword with fists, and backs away from you.","","The knight's armored fist hits you straight in the face. He topples over, but you're left with a bruise.",0,0,"","","",0,0,12,14,4,0),
       ("Shrine","A holy glow radiates from between the trees. A stone shrine is sitting in a clearing in the woods, surrounded by offerings.","shrine_map.png",1,"The guardian spirit emerge from the shrine, he wants to ask you a riddle before you pass","guargian.png","","","The guardian seems to be pleased with your answer and grant you some gold","","The guardian looks dissapointed, this wasn't the answer they looked for",0,0,"","","",15,0,13,0,0,1),
       ("Scholar's Lair","A twirling tower looms above you. You see books, tomes and scrolls inside, and a strong arcane energy fills the air","lair_map.png",0,"","","","","","","",1,5,"cloak.png","Invisible Cloak","on your way you find a wierdly shaped house, you carefully walk inside and trip over a piece of cloth. as you pick it up, your hand become invisble, it might be useful later, would you keep it?",0,14,7,0,0,0),
       ("Hut","A worn-down hut stands near the entrance to the forest. An old man is sitting on the porch, carving a wooden figure. From the looks of it, he is making a wooden wolf.","hut_map.png",1,"The old man looks at you and says: I have some gift for you, kid. But you only get it if you answer my riddle correctly.","oldMan.png","","","You answer the old man riddle correctly, he hand you some gold","","That was not the correct answer for the old man riddle, you leave empty handed",0,0,"","","",12,0,2,0,0,1),
       ("Chapel","A sense of dread sits in your stomach as you approach the cold, stone walls of a chapel. The air inside is damp, and the very ground beneath your feet seems to hold its breath.","chapel_map.png",0,"","","","","","","",1,6,"chalice.png","Holy Chalice","On the dusty altar you find a chalice, somehow it makes you feel better. Do you take it?",18,0,0,4,0,0),
       ("Cave","You approach an opening in the mountain which is covered in stalactites. The cave looks like a beast, baring its teeth at you.","cave_map.png",0,"","","","","","","",1,7,"shield.png","Shield","near to a huge rock there is something shiny, as you get closer you find a shield attached to a skeleton, would you take it?",19,17,0,8,0,0),
       ("Troll Hideout","A putrid smell hits your nose as you find yourself face-to-face with three hulking figures - trolls!","trollHideout_map.png",1,"despite their appearance, they seem to be friendly one them walks closer to you and suddenly ask you a question","troll.png","","","The troll claps his hands out of satisfaction and hands you a pouch of gold","","The Troll shake his head and he looks very dissapointed by your answer",0,0,"","","",0,18,0,20,0,1),
       ("Marsh","Your feet stick to the ground as you make your way through a marsh. A thick fog obscures your vision as you follow the near-invisible path. Despite the fog, you're certain something is watching you.","marsh_map.png",0,"","","","","","","",0,0,"","","",21,8,19,0,0,0),
       ("Broken Portal","A lone stone structure lies ahead of you, shattered and broken. The grass around it is burnt, and you find strange objects around it - items not from this world, you''re certain.","brokenPortal_map.png",1,"As you approach the portal start to glow faintly. a whisper comes from the swerling glow. it is a question for you","portal.png","","","The portal start to glow brigther and some gold falls throught it","","The portal starts to spark and after a brigh glow, it becomes dark and doesn't respond to you anymore",0,0,"gemstone.png","Gemstone","",0,20,0,22,0,1),
       ("Bone Field","The stones under your feet turn lighter and lighter, until you realise they're not stones at all. The field ahead of you shines an ivory white, full of bones of various sizes and sources. What brought them here? You'd rather not think about it too much.","boneField_map.png",0,"","","","","","","",0,0,"","","",0,9,21,23,0,0),
       ("Wolf","You hear pained whining coming from underneath a fallen tree a wolf has been trapped underneath! It's trying to free itself, but seems to be making no progress.","wolf_map.png",0,"","","","","","","",0,0,"","","",0,10,22,0,0,0),
       ("Demogorgon Room","You hear growling nearby","demogorgon_room_map.png",1,"You see a gigantic beast in front of you, showing its humongous fangs.","demogorgon.png","","","","","",0,0,"","","",0,0,0,0,0,0),
       ("Exit","Congratulations! you have find the exit.","exit.png",0,"","","","","","","",0,0,"","","",0,0,0,0,0,0);

insert into current_game(player, current_location, inventory, score)
values ("", 1, 1, 0)


