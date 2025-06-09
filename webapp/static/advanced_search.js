/*
 * advanced_search.js
 * Daniel, Soren, Indy
 * Adapted from Jeff Ondich's 'books.js'
 */

window.addEventListener("load", initialize);

function initialize() {
    // loads everything
    loadSeasonsSelector();
    loadEventsSelector();
    loadTeamsSelector();
    loadMeetSelector();

    let selectButton = document.getElementById('selectButton');  // When select function clicked, toggles teams all clicked or not
    if (selectButton) {
        selectButton.onclick = toggleTeams;
    }

    let selectSeason = document.getElementById('seasonSelect'); // When a new season is selected, updates the meets dropdown
    if (selectSeason) {
        selectSeason.onchange = loadMeetSelector;
    }

    let form = document.getElementById('advancedSearchForm');
    if (form) {
        form.addEventListener('submit', function (e) { // when form is clicked
            e.preventDefault();
            const formData = new FormData(form);
            const params = new URLSearchParams();

            for (const [key, value] of formData.entries()) { // manually grab the params and update the URL
                if (value) params.append(key, value);
            }

            history.pushState(null, '', '?' + params.toString()); // push the converted url with params
            onSearch(); // queries as normal
        });
    }
}


// Returns the base URL of the API, onto which endpoint components can be appended.
function getAPIBaseURL() {
    let baseURL = window.location.protocol
        + '//' + window.location.hostname
        + ':' + window.location.port
        + '/api';
    return baseURL;
}


function loadMeetSelector() { // populates meet dropdown with meets (from specified season if applicable)
    let selectElement = document.getElementById('seasonSelect');
    season = selectElement.value;
    if (season) {
        season = '?season=' + season;
    }
    let url = getAPIBaseURL() + '/meets/' + season;

    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function (result) {
            let selectorBody = '';
            for (let k = 0; k < result.length; k++) {
                let meet = result[k];
                if (k == 0) {
                    selectorBody += '<option selected=True name="meet" value="' + '' + '">' + 'All Meets' + '</option>\n';
                } else {
                    selectorBody += '<option name="meet" value="' + meet['meet_name'] + '">' + meet['meet_name'] + '</option>\n';
                }
            }
            let selector = document.getElementById('meetSelect');
            if (selector) {
                selector.innerHTML = selectorBody;
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}


function loadEventsSelector() { // populates event dropdown with all events (no repeats, default)
    let url = getAPIBaseURL() + '/events/';
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function (result) {
            let selectorBody = '';
            for (let k = 0; k < result.length; k++) {
                let event = result[k];
                if (k == 0) {
                    selectorBody += '<option selected=True name="event" value="' + event['event_name'] + '">' + event['event_name'] + '</option>\n';
                } else {
                    selectorBody += '<option name="event" value="' + event['event_name'] + '">' + event['event_name'] + '</option>\n';
                }
            }
            let selector = document.getElementById('eventSelect');
            if (selector) {
                selector.innerHTML = selectorBody;
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}


function loadSeasonsSelector() { // populates seasons dropdown with all seasons
    let url = getAPIBaseURL() + '/seasons/';
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function (result) {
            let selectorBody = '';
            for (let k = 0; k < result.length; k++) {
                let season = result[k];
                if (k == 0) {
                    selectorBody += '<option selected=True name="event" value="' + '' + '">' + 'All Seasons' + '</option>\n';
                } else {
                    selectorBody += '<option name="event" value="' + season['season_name'] + '">' + season['season_name'] + '</option>\n';
                }
            }
            let selector = document.getElementById('seasonSelect');
            if (selector) {
                selector.innerHTML = selectorBody;
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}


function loadTeamsSelector() { // loads teams select buttons with all teams from dataset
    let url = getAPIBaseURL() + '/teams/';
    fetch(url, { method: 'get' })
        .then((response) => response.json())
        .then(function (result) {
            let teamsBody = '<h6>Team Select</h6>';
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
        .catch(function (error) {
            console.log(error);
        });
}


function onSearch() { // Main search function - runs query twice, once for each gender tab
    const genders = ['m', 'f'];
    for (let i = 0; i < genders.length; i++) {
        const gender = genders[i];
        const currentParams = window.location.search;
        url = getAPIBaseURL() + '/search' + currentParams + '&gender=' + gender;

        fetch(url, { method: 'get' })
            .then((response) => response.json())
            .then(function (searchResult) {
                let listBody = '';
                let tableHeader =
                    '<table class="table rounded-3 overflow-hidden text-center align-middle">\n' +
                    '<thead class="table-dark">\n<tr><th scope="col">#</th><th scope="col">Name</th><th scope="col">Team</th><th scope="col">Mark</th><th scope="col">Meet</th><th scope="col">Season</th><th scope="col">Date</th></tr>\n</thead>\n';

                let tableBody = '';
                tableBody += tableHeader + '\n<tbody>';

                for (let j = 0; j < searchResult.length; j++) {
                    let performance = searchResult[j];
                    let tableRow = '';

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
                    }
                } else {
                    let performanceList = document.getElementById('women-tab-pane');
                    if (performanceList) {
                        performanceList.innerHTML = listBody;
                    }
                }

                performanceListContainer = document.getElementById('performanceListContainer');
                if (performanceListContainer.classList.contains('d-none')) {
                    performanceListContainer.classList.remove('d-none');
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    }
}


function toggleTeams() { // toggles whether all teams are selected or not
    let selectButton = document.getElementById('selectButton');
    let checked = !(selectButton.getAttribute('value') === 'true');

    let checkboxes = document.querySelectorAll('input[name="team"]');
    checkboxes.forEach((checkbox) => {
        checkbox.checked = checked;
    });

    if (checked) {
        selectButton.setAttribute('value', 'true');
        selectButton.classList.remove('btn-success');
        selectButton.classList.add('btn-danger');
        selectButton.innerText = 'Deselect all teams';
    } else {
        selectButton.setAttribute('value', 'false');
        selectButton.classList.remove('btn-danger');
        selectButton.classList.add('btn-success');
        selectButton.innerText = 'Select all teams';
    }
}
