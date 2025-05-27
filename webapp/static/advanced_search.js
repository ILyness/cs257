/*
 * advanced_search.js
 * Daniel, Soren, Indy
 * Adapted from Jeff Ondich's 'books.js'
 */

window.addEventListener("load", initialize);

function initialize() {
    onSearch();
    let form = document.getElementById('advancedSearchForm');
    if (form) {
        form.onsubmit = onSearch;
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

function onSearch() {
    let url = getAPIBaseURL() + '/search?';

    let event = document.getElementById('event').value;
    //let genderMen = document.getElementById('genderMen');
    let gender = document.getElementById('gender');
   // let duplicatesTrue = document.getElementById('duplicatesTrue');
    let duplicates = document.getElementById('duplicates');
    let team = document.getElementById('team');
    let season = document.getElementById('season');
    let meet = document.getElementById('meet');
    let mark = document.getElementById('mark');

  //  if (genderMen.value = )

    url += event;
    url += gender;
    url += duplicates;
    url += team;
    url += season;
    url += meet;
    url += mark;

    console.log("url = ", url);

    fetch(url, {method: 'get'})
    .then((response) => response.json())
    .then(function(searchResult) {
        console.log("running onSearch JS")
        console.log("searchResult", searchResult)
        let listBody = '';
        let keys = Object.keys(searchResult)
        let tableHeader = '<table class="table rounded-3 overflow-hidden text-center align-middle">\n' +
                            '<thead class="table-dark">\n<tr><th scope="col">#</th><th scope="col">Name</th><th scope="col">Team</th><th scope="col">Mark</th><th scope="col">Meet</th><th scope="col">Season</th><th scope="col">Date</th></tr>\n</thead>\n'
        for (let k = 0; k < keys.length; k++) {
            
            let event = keys[k];
            let tableBody = '';
            tableBody += '<h5>' + event + '</h5>\n'
                                + tableHeader
                                + '\n<tbody>';
            let performances = searchResult[event]

            for (let j = 0; j < performances.length; j++) {
                let performance = performances[j]
                let tableRow = ''
                console.log("filling table with a row from performance search results")
                tableRow += '<tr>\n<th scope="row">' + (j+1) + '</th>' +
                                '<td class="col-md-3">' + performance['athlete_name'] + '</td>' +
                                '<td class="col-md-2">' + performance['team'] + '</td>' +
                                '<td class="col-md-2">' + performance['mark'] + '</td>' +
                                '<td class="col-md-3">' + performance['meet'] + '</td>' +
                                '<td class="col-md-2">' + performance['season_name'] + '</td>' +
                                '<td class="col-md-2">' + performance['result_date'] + '</td>' +
                                '\n</tr>\n';
                tableBody += tableRow
            }
            let tableRow = ''
                tableRow += '<tr>\n<th scope="row">' + (1) + '</th>' +
                                '<td class="col-md-3">' + "HI!!!" + '</td>' +
                                '<td class="col-md-2">' + "HI!!!" + '</td>' +
                                '<td class="col-md-2">' + "HI!!!" + '</td>' +
                                '<td class="col-md-3">' + "HI!!!" + '</td>' +
                                '<td class="col-md-2">' + "HI!!!" + '</td>' +
                                '<td class="col-md-2">' + "HI!!!" + '</td>' +
                                '\n</tr>\n';
                tableBody += tableRow
            tableBody += '</tbody>\n</table>\n'
            listBody += tableBody
            
        }

        let performanceList = document.getElementById('advancedSearchTable')
        const test = 'is this thing on?'
        const testE = document.getElementById('test')
        if (testE) {
            testE.textContent = test;
        }
        if (performanceList) {
            performanceList.innerHTML = listBody;
        }
        console.log("list body ", listBody)
    })

    .catch(function(error) {
        console.log(error);
    });
}