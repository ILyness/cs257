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

function onSearch() {
    let url = getAPIBaseURL() + '/search';
    console.log("url = ", url);

    const currentParams = window.location.search;
    url = getAPIBaseURL() + '/search' + currentParams;
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

            let performanceList = document.getElementById('advancedSearchTable');

            if (performanceList) {
                performanceList.innerHTML = listBody;
            }

            console.log("list body ", listBody);
        })
        .catch(function (error) {
            console.log(error);
        });
}


