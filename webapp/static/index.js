/*
 * index.js
 * Daniel, Soren, Indy
 * Adapted from Jeff Ondich's 'books.js'
 */

window.addEventListener("load", initialize);

function initialize() {
    let selectElement = document.getElementById('seasonSelect');
    if (selectElement) {
        selectElement.onchange = loadEventsSelector;
    }
    loadSeasonsSelector();
    let form = document.getElementById('filterForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        loadPerformanceList();
    });
    let selectButton = document.getElementById('selectButton');
    if (selectButton) {
        selectButton.onclick = toggleEvents;
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
    let selectElement = document.getElementById('seasonSelect');
    let season = selectElement.value;
    let url = getAPIBaseURL() + '/events/?season=' + season;

    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(result) {
        let eventsBody = ''
        for (let k = 0; k < result.length; k++) {
            let event = result[k]['event_name'];
            if (k % 5 == 0) {
                if (k > 0) {
                    eventsBody += '</div>\n';
                }
                eventsBody += '<div class="col-md-2">\n';
            }
            eventsBody += `
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" name="event" id="event${event.split(' ')[0]}" value="${event}" checked="true"/>
                  <label class="form-check-label" for="event${event.split(' ')[0]}">${event}</label>
                </div>\n
            `;
        }
        let selector = document.getElementById('eventSelect');
        if (selector) {
            selector.innerHTML = eventsBody;
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
            loadEventsSelector();
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}

function loadPerformanceList() {
    let selectElement = document.getElementById('seasonSelect');
    season = selectElement.value;
    
    
    let url = getAPIBaseURL() + '/list/?season=' + season;

    // Send the request to the books API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(result) {
        // Add the <option> elements to the <select> element
        let checkboxes = document.querySelectorAll('input[name="event"]:checked');
        let events = Array.from(checkboxes).map((checkbox) => checkbox.value);
        categories = Object.keys(result)
           let tableHeader = '<table class="table rounded-3 overflow-hidden text-center align-middle">\n' +
                            '<thead class="table-dark">\n<tr><th scope="col">#</th><th scope="col">Name</th><th scope="col">School</th><th scope="col">Mark</th><th scope="col">Meet</th><th scope="col">Date</th></tr>\n</thead>\n'
        for (let j = 0; j < categories.length; j++) {
            let listBody = '';
            let category = categories[j];
            let keys = Object.keys(result[category]);
            for (let k = 0; k < keys.length; k++) {
                let event = keys[k];
                if (!(events.includes(event))) {
                    continue
                }
                let performances = result[category][event];
                if (performances.length == 0) {
                    continue
                }
                let tableBody = '';
                tableBody += '<h5>' + event + '</h5>\n'
                                    + tableHeader
                                    + '\n<tbody>';
                for (let j = 0; j < performances.length; j++) {
                    performance = performances[j]
                    let tableRow = ''
                    tableRow += '<tr>\n<th scope="row">' + (j+1) + '</th>' +
                                    '<td class="col-md-3">' + performance['athlete_name'] + '</td>' +
                                    '<td class="col-md-2">' + performance['school'] + '</td>' +
                                    '<td class="col-md-2">' + performance['mark'] + '</td>' +
                                    '<td class="col-md-3">' + performance['meet'] + '</td>' +
                                    '<td class="col-md-2">' + performance['date'] + '</td>' +
                                    '\n</tr>\n';
                    tableBody += tableRow;
                }
                tableBody += '</tbody>\n</table>\n';
                listBody += tableBody;
            }
            if (category == 'm') {
                let performanceList = document.getElementById('men-tab-pane');
                if (performanceList) {
                    performanceList.innerHTML = listBody;
                }
            }
            else {
                let performanceList = document.getElementById('women-tab-pane');
                    if (performanceList) {
                    performanceList.innerHTML = listBody;
                }
            }
        }


        performanceListContainer = document.getElementById('performanceListContainer');
        if (events.length == 0) {
            if (!(performanceListContainer.classList).contains('d-none')) {
                performanceListContainer.classList.add('d-none');
            }
        }
        else {
            if (performanceListContainer.classList.contains('d-none')) {
                performanceListContainer.classList.remove('d-none');
            }
        }


    })

   
    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}

function toggleEvents() {
    let selectButton = document.getElementById('selectButton');
    let checked = !(selectButton.getAttribute('value') === 'true');

    let checkboxes = document.querySelectorAll('input[name="event"]');
    checkboxes.forEach((checkbox) => {
        checkbox.checked = checked;
    })

    if (checked) {
        selectButton.setAttribute('value', 'true');
        selectButton.classList.remove('btn-success');
        selectButton.classList.add('btn-danger')
        selectButton.innerText = 'Deselect all events';
    }
    else {
        selectButton.setAttribute('value', 'false');
        selectButton.classList.remove('btn-danger');
        selectButton.classList.add('btn-success')
        selectButton.innerText = 'Select all events';
    }

}
