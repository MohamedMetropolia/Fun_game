'use strict';

const loginErrorMsg = document.getElementById("login-error-msg");
loginErrorMsg.style.opacity = 1

const apiUrl = 'http://127.0.0.1:5000/';

document.querySelector('#player-form').addEventListener('submit', function (evt) {
  evt.preventDefault();
  const playerNamee = document.querySelector('#player-input').value;
  document.querySelector('#player-modal').classList.add('hide');
  gameSetup(`${apiUrl}newgame?player=${playerNamee}&loc=${startLoc}`);
});

// function to fetch data from API
async function getData(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error('Invalid server input!');
  const data = await response.json();
  return data;
}
// function to set up game
// this is the main function that creates the game and calls the other functions
async function gameSetup(url) {
  try {
    document.querySelector('.goal').classList.add('hide');
    airportMarkers.clearLayers();
    const gameData = await getData(url);
    console.log(gameData);
    updateStatus(gameData.status);
    if (!checkGameOver(gameData.status.co2.budget)) return;
    for (let airport of gameData.location) {
      const marker = L.marker([airport.latitude, airport.longitude]).addTo(map);
      airportMarkers.addLayer(marker);
      if (airport.active) {
        map.flyTo([airport.latitude, airport.longitude], 10);
        showWeather(airport);
        checkGoals(airport.weather.meets_goals);
        marker.bindPopup(`You are here: <b>${airport.name}</b>`);
        marker.openPopup();
        marker.setIcon(greenIcon);
      } else {
        marker.setIcon(blueIcon);
        const popupContent = document.createElement('div');
        const h4 = document.createElement('h4');
        h4.innerHTML = airport.name;
        popupContent.append(h4);
        const goButton = document.createElement('button');
        goButton.classList.add('button');
        goButton.innerHTML = 'Fly here';
        popupContent.append(goButton);
        const p = document.createElement('p');
        p.innerHTML = `Distance ${airport.distance}km`;
        popupContent.append(p);
        marker.bindPopup(popupContent);
        goButton.addEventListener('click', function () {
          gameSetup(`${apiUrl}flyto?game=${gameData.status.id}&dest=${airport.ident}&consumption=${airport.co2_consumption}`);
        });
      }
    }
    updateGoals(gameData.goals);
  } catch (error) {
    console.log(error);
  }
}

function askPlayerName() {
  // prompt user for name
  const playerName = document.querySelector('#player_name').value;
  gameSetup(`${apiUrl}newgame?player=${playerName}&loc=${startLoc}`);
});
  // set the required variables, if needed

  //return name
  return playerName;
}


async function postToApi(postToApiUrl) {
    const settings = {
        method: 'POST',
        headers: {
            Accept: 'application/json',
            'Content-Type': 'application/json',
        }
    };
    try {
        const fetchResponse = await fetch(`http://127.0.0.1:5000/`, settings);
        const data = await fetchResponse.json();
        return data;
    } catch (e) {
        return e;
    }
}


function initGame(playerName) {
  // call api to create user
  let postToApiUrl = apiUrl + "/create_player/" + playerName; //todo: create api in flask
  return postToApi(postToApiUrl);
}

function fetchLocation(number) {
  return getData(apiUrl + "/location/" + number)
}

//player movement to new area
function moveHandlerUp(evt) {
  evt.preventDefault();
  let moveResponse = sendMoveToApi(apiUrl + "/move/up")
  renderLocation(moveResponse);
}

function moveHandlerDown(evt) {
  evt.preventDefault();
  let moveResponse = sendMoveToApi(apiUrl + "/move/down")
  renderLocation(moveResponse);
}

function moveHandlerRight(evt) {
  evt.preventDefault();
  let moveResponse = sendMoveToApi(apiUrl + "/move/right")
  renderLocation(moveResponse);
}

function moveHandlerLeft(evt) {
  evt.preventDefault();
  let moveResponse = sendMoveToApi(apiUrl + "/move/left")
  renderLocation(moveResponse);
}

function renderLocation(location) {
  //hide all map pieces
  document.querySelector('.map').classList.add('hide');
  //this is already a JS object

  //add player name, location and item to the correct field in the document
  document.querySelector('username').innerHTML = `Username: ${playerName}`
  document.querySelector('current_item').innerHTML = `Current item: ${item}` //todo: define current item variable
  document.querySelector('current_location').innerHTML = `Current location: ${location}`
  //render map

  //add location text to the html
  document.querySelector('.gametext').innerHTML = locationText //todo: needs to be defined

  //if there is item pick up, unhide item pick up section
  //display all options with the flavour text
  //add item pick up button handlers
  //call the pick up api to add the item to the player

  //unhide encounter section if there is any
  //add any flavour text and great art of anscii and other image to the page
  //add the handlers like the item handlers top the buttons

  //add correct links to restart and quit buttons

  //add move handlers to the buttons and/or to the WASD keys, but only to those that we allow from location


}

//start game function
function startGame() {
  //ask for player name
  let playerName = askPlayerName()
  // init game in python with the player name
  let initGameResponse = initGame(playerName)
  //check if init game was successful
  //if (!initGameResponse.ok)....
  //start loading image

  //get first area data
  let startLoc = fetchLocation(1) //fetch first location
  //hide loading image

  //parse location data and add it to html
  renderLocation(firstLocation)

}

//this is what we will use to parse move_response

// event listener to hide goal splash
document.querySelector('.goal').addEventListener('click', function (evt) {
  evt.currentTarget.classList.add('hide');
});