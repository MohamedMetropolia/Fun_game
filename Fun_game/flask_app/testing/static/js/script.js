'use strict';

const apiUrl = 'http://127.0.0.1:5000/';

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
        goButton.addEventListener('click', function() {
          gameSetup(
              `${apiUrl}flyto?game=${gameData.status.id}&dest=${airport.ident}&consumption=${airport.co2_consumption}`);
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
    },
  };
  try {
    const fetchResponse = await fetch(`${postToApiUrl}`, settings);
    const data = await fetchResponse.json();
    return data;
  } catch (e) {
    return e;
  }
}

function initGame(playerName) {
  // call api to create user
  let postToApiUrl = apiUrl + 'create_player/' + playerName; //todo: create api in flask
  return postToApi(postToApiUrl);
}

function fetchLocation(number) {
  return getData(apiUrl + 'location/' + number);
}

//player movement to new area
async function moveHandlerUp(evt) {
  evt.preventDefault();
  const moveResponse = await postToApi(apiUrl + 'move/up');
  renderLocation(moveResponse);
}

async function moveHandlerDown(evt) {
  evt.preventDefault();
  let moveResponse = await postToApi(apiUrl + 'move/down');
  renderLocation(moveResponse);
}

async function moveHandlerRight(evt) {
  evt.preventDefault();
  let moveResponse = await postToApi(apiUrl + 'move/right');
  renderLocation(moveResponse);
}

async function moveHandlerLeft(evt) {
  evt.preventDefault();
  let moveResponse = await postToApi(apiUrl + 'move/left');
  renderLocation(moveResponse);
}

function renderLocation(location) {
  //hide all map pieces
  console.log(location);
  if (location.map_image !== undefined) {
    //alert(location.map_image)
    //document.getElementById(".map").src = location.map_image;
  }
  //add player name, location and item to the correct field in the document
  document.querySelector('#username').innerHTML = `Username: ${location.player_name}`;
  // if there is an inventory.description then we have an item, display item desc and image
  document.querySelector('#current_item').innerHTML = `Current item: ${location.item.description}`;
  document.querySelector('#current_location').innerHTML = `Current location: ${location.location_name}`;
  //add location text to the html
  document.querySelector('#textbox').innerHTML = location.location_text;

  //if there is item pick up, unhide item pick up section
  if (location.item.id) {
    document.querySelector('#item_pickup').classList.remove('hide');
    document.querySelector('#item_pickup_text').innerHTML = location.item_decision.item_decision_text;
    document.querySelector('#item_yes_button').addEventListener('click', function(evt) {
          getData(location.item_decision.options[0].api_url);
          //registering new item in database
          document.querySelector('#item_pickup').classList.add('hide');
        });
    document.querySelector('#item_no_button').
        addEventListener('click', function(evt) {
          document.querySelector('#item_pickup').setAttribute('style', 'display:none');
        });
  }

  //encounter section
  if (location.encounter.encounter_text !== "") {
    document.querySelector('#item_pickup').classList.add('hide');
    document.addEventListener('input', function(evt) {
      let riddleUserInput = document.getElementById('riddle_user_input').value;
      if (riddleUserInput.toLowerCase() === location.encounter.riddle_answer.toLowerCase()) {
        document.querySelector('#item_pickup').classList.remove('hide');
      }
      else {
        if (riddleUserInput === '') {
          document.querySelector('#riddle_correct_answer').setAttribute('style', 'display:none');  //we need DIS and show with display:block to hide tags
        } else {
          document.querySelector('#riddle_correct_answer').innerHTML = `Correct answer: ` +
              location.encounter.riddle_answer;
          document.querySelector('#riddle_correct_answer').classList.remove('hide');
        }
      }

      document.querySelector('#encounter').classList.remove('hide');
      document.querySelector('#encounter_text').innerHTML = location.encounter.encounter_text;
      document.querySelector('#riddle_question').innerHTML = location.encounter.riddle_question;

    });
  }

  //correct links to restart and quit buttons
  document.querySelector('#restart_button').addEventListener('click', function(evt) {
          window.location.href = apiUrl + '/home'
        });
  document.querySelector('#quit_button').addEventListener('click', function(evt) {
          window.location.href = apiUrl + '/gameover'
        });

  //move handlers to the buttons and/or to the WASD keys, but only to those that we allow from location
  async function keyMove(event) {
    if (event.isComposing || event.keyCode === 87) {
      let moveResponse = await postToApi(apiUrl + 'move/up');
      renderLocation(moveResponse);
    } else if (event.isComposing || event.keyCode === 83) {
      let moveResponse = await postToApi(apiUrl + 'move/down');
      renderLocation(moveResponse);
    } else if (event.isComposing || event.keyCode === 65) {
      let moveResponse = await postToApi(apiUrl + 'move/left');
      renderLocation(moveResponse);
    } else if (event.isComposing || event.keyCode === 68) {
      let moveResponse = await postToApi(apiUrl + 'move/right');
      renderLocation(moveResponse);
    }
  }
  document.addEventListener("keydown", keyMove);
}

//start game function
function startGame() {
  //ask for player name
  let playerName = askPlayerName();
  // init game in python with the player name
  let initGameResponse = initGame(playerName);
  //check if init game was successful
  //if (!initGameResponse.ok)....
  //start loading image

  document.querySelector('#loader').classList.add('hide');
  //get first area data
  let startLoc = fetchLocation(1); //fetch first location
  //hide loading image

  document.querySelector('#loader').classList.remove('hide');
  //parse location data and add it to html
  renderLocation(firstLocation);

}

//mock render for testing
async function mock() {
  let moveResponse = await postToApi(apiUrl + 'move/left');
  renderLocation(moveResponse);
}

mock();