/*
 * advanced_search.js
 * Daniel, Soren, Indy
 * Adapted from Jeff Ondich's 'books.js'
 */


window.addEventListener("load", initialize);


function initialize() {
    loadSeasonsSelector();
    loadEventsSelector();
    loadTeamsSelector();
    let selectButton = document.getElementById('selectButton');
    if (selectButton) {
        selectButton.onclick = toggleEvents;
    }
    let form = document.getElementById('advancedSearchForm');
    if (form) {
    form.addEventListener('submit', function (e) { /* HERE IS THE CHANGE I MADE */
        e.preventDefault();
        const formData = new FormData(form);
        const params = new URLSearchParams();

            for (const [key, value] of formData.entries()) { // THIS SHOULD MANUALLY GRAB THE PARAMS FROM THE URL AND UPDATE THE URL WITH THE VARIABLES AND THEN NOT RELOAD
                if (value) params.append(key, value);
            }


            history.pushState(null, '', '?' + params.toString()); // pushes the converted url with prams

           


            onSearch(); //queries as normal
    });
    }
}


// Returns the base URL of the API, onto which endpoint
// components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
                    + '//' + window.location.hostname
                    + ':' + window.location.port
                    + '/api';
    return baseURL;
}


 function loadEventsSelector() {
    let url = getAPIBaseURL() + '/events/';
    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(result) {
        let selectorBody = ''
        for (let k = 0; k < result.length; k++) {
            let event = result[k];
            if (k == 0) {
                selectorBody += '<option selected=True name="event" value="' + event['event_name'] + '">' + event['event_name'] + '</option>\n';
            }
            else {
                selectorBody += '<option name="event" value="' + event['event_name'] + '">' + event['event_name'] + '</option>\n';
            }
        }
        let selector = document.getElementById('eventSelect');
       // document.getElementById("eventSelect").style.height = "20px";
        if (selector) {
            selector.innerHTML = selectorBody;
            //loadEventsSelector();
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function loadSeasonsSelector() {
    let url = getAPIBaseURL() + '/seasons/';

    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(result) {

        let selectorBody = ''
        for (let k = 0; k < result.length; k++) {
            let season = result[k];
            if (k == 0) {
                selectorBody += '<option selected=True name="event" value="' + season['season_name'] + '">' + season['season_name'] + '</option>\n';
            }
            else {
                selectorBody += '<option name="event" value="' + season['season_name'] + '">' + season['season_name'] + '</option>\n';
            }
        }
        let selector = document.getElementById('seasonSelect');
        if (selector) {
            selector.innerHTML = selectorBody;
            //loadEventsSelector();
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function loadTeamsSelector() {
   // let selectElement = document.getElementById('teamSelect');
    //let team = selectElement.value;
    let url = getAPIBaseURL() + '/teams/';

    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(result) {
        let teamsBody = '<h6>Team Select</h6>'
        for (let k = 0; k < result.length; k++) {
            let team = result[k]['school_name'];
            if (k % 1 == 0) {
                if (k > 0) {
                    teamsBody += '</div>\n';
                }
                teamsBody += '<div class="col-md-2">\n';
            }
            teamsBody += `
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" name="team" id="team${team.split(' ')[0]}" value="${team}" checked="true"/>
                  <label class="form-check-label" for="team${team.split(' ')[0]}">${team}</label>
                </div>\n
            `;
        }
        let selector = document.getElementById('teamSelect');
        if (selector) {
            selector.innerHTML = teamsBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}



function onSearch() {

   // let url = getAPIBaseURL() + '/search';
 //   console.log("url = ", url);
    const genders = ['m','f']
    for (let i = 0; i < genders.length; i++) {
        const gender = genders[i];
        const currentParams = window.location.search;
        url = getAPIBaseURL() + '/search' + currentParams + '&gender=' + gender;
        console.log("url = ", url);

        fetch(url, { method: 'get' })
            .then((response) => response.json())
            .then(function (searchResult) {
                console.log("running onSearch JS");
                console.log("searchResult", searchResult);

                let listBody = '';

                let tableHeader = '<table class="table rounded-3 overflow-hidden text-center align-middle">\n' +
                    '<thead class="table-dark">\n<tr><th scope="col">#</th><th scope="col">Name</th><th scope="col">Team</th><th scope="col">Mark</th><th scope="col">Meet</th><th scope="col">Season</th><th scope="col">Date</th></tr>\n</thead>\n';

                let tableBody = '';
                tableBody +=  tableHeader + '\n<tbody>';

                for (let j = 0; j < searchResult.length; j++) {
                    let performance = searchResult[j];
                    let tableRow = '';
                    console.log("filling table with a row from performance search results");
                    tableRow += '<tr>\n<th scope="row">' + (j + 1) + '</th>' +
                        '<td class="col-md-3">' + performance['athlete_name'] + '</td>' +
                        '<td class="col-md-2">' + performance['team'] + '</td>' +
                        '<td class="col-md-2">' + performance['mark'] + '</td>' +
                        '<td class="col-md-3">' + performance['meet'] + '</td>' +
                        '<td class="col-md-2">' + performance['season_name'] + '</td>' +
                        '<td class="col-md-2">' + performance['result_date'] + '</td>' +
                        '\n</tr>\n';
                    tableBody += tableRow;
                }

                tableBody += '</tbody>\n</table>\n';
                listBody += tableBody;
                if (gender == 'm') {
                    let performanceList = document.getElementById('men-tab-pane');
                    if (performanceList) {
                        performanceList.innerHTML = listBody;
                        console.log("filling men table");

                    }
                }
                else {
                    let performanceList = document.getElementById('women-tab-pane');
                        if (performanceList) {
                        performanceList.innerHTML = listBody;
                        console.log("filling women table");
                    }
                }
            //just run twice with no if......

                
            })
            .catch(function (error) {
                console.log(error);
            });
        }
    }

function toggleEvents() {
    let selectButton = document.getElementById('selectButton');
    let checked = !(selectButton.getAttribute('value') === 'true');

    let checkboxes = document.querySelectorAll('input[name="team"]');
    checkboxes.forEach((checkbox) => {
        checkbox.checked = checked;
    })

    if (checked) {
        selectButton.setAttribute('value', 'true');
        selectButton.classList.remove('btn-success');
        selectButton.classList.add('btn-danger')
        selectButton.innerText = 'Deselect all teams';
    }
    else {
        selectButton.setAttribute('value', 'false');
        selectButton.classList.remove('btn-danger');
        selectButton.classList.add('btn-success')
        selectButton.innerText = 'Select all teams';
    }

}

