/*
 * index.js
 * Daniel, Soren, Indy
 * Adapted from Jeff Ondich's 'books.js'
 */

window.addEventListener("load", initialize);

function initialize() {
    let element = document.getElementById('ButtonGetData');
    if (element) {
        element.onclick = onGetData;
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

function onGetData() {
    let url = getAPIBaseURL() + '/list/';

    // Send the request to the books API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(result) {
        // Add the <option> elements to the <select> element
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

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}
