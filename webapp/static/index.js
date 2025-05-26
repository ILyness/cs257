/*
 * index.js
 * Daniel, Soren, Indy
 * Adapted from Jeff Ondich's 'books.js'
 */

window.addEventListener("load", initialize);

function initialize() {
    loadSeasonsSelector();
    let element = document.getElementById('ButtonGetData');
    if (element) {
        element.onclick = onGetData;
    }
    let form = document.getElementById('filterForm');
    if (form) {
        form.onsubmit = loadPerformanceList;
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

function loadSeasonsSelector() {
    let url = getAPIBaseURL() + '/seasons/'

    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(result) {
        let selectorBody = '<option value="" selected>Choose season...</option>\n'
        for (let k = 0; k < result.length; k++) {
            let season = result[k]
            selectorBody += '<option value="' + season['season_name'] + '">' + season['season_name'] + '</option>\n'
        }
        let selector = document.getElementById('seasonSelect');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })
}

function onGetData() {
    //dawdawd awd w
    let url = getAPIBaseURL() + '/list/';
// html call this and implements
//get element by ID
//.selected
    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(result) {
        let listBody = '';
        keys = Object.keys(result)
        let tableHeader = '<table class="table rounded-3 overflow-hidden text-center align-middle">\n' +
                            '<thead class="table-dark">\n<tr><th scope="col">#</th><th scope="col">Name</th><th scope="col">School</th><th scope="col">Mark</th><th scope="col">Meet</th><th scope="col">Date</th></tr>\n</thead>\n'
        for (let k = 0; k < keys.length; k++) {
            let event = keys[k];
            let tableBody = '';
            tableBody += '<h5>' + event + '</h5>\n'
                                + tableHeader
                                + '\n<tbody>';
            let performances = result[event]
            if (performances.length < 10) {
                continue
            }
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
                tableBody += tableRow
            }
            tableBody += '</tbody>\n</table>\n'
            listBody += tableBody
        }

        let performanceList = document.getElementById('performance_list');
        if (performanceList) {
            performanceList.innerHTML = listBody;
        }
    })

    .catch(function(error) {
        console.log(error);
    });
}
