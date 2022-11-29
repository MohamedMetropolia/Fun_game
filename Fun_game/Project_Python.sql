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
    PRIMARY KEY (id)
);
create table current_game
(
     id               int(11) NOT NULL AUTO_INCREMENT,
     player           varchar(40) DEFAULT NULL,
     current_location int(40)     DEFAULT NULL,
     inventory        int(40) DEFAULT NULL,
     score            int(40) DEFAULT null,
     last_updated     timestamp,
    PRIMARY KEY (id),
    FOREIGN KEY (current_location) REFERENCES location (id),
    FOREIGN KEY (inventory) REFERENCES items(id)
);
# Adding the data to the tables
insert into items(description)
values ("Nothing"),
       ("feather"),
       ("Gold"),
       ("Sword");

insert into location(description)
values ("Maze"),
       ("Basement"),
       ("Crossroad"),
       ("Graveyard"),
       ("Forest"),
       ("Necropolis"),
       ("Fork"),
       ("Treasure Room"),
       ("Cementery"),
       ("Shed");

insert into current_game(player, current_location, inventory, score)
values ("Starting player", 1, 1, 0)


