/*
 * index.js
 * Daniel, Soren, Indy
 * Adapted from Jeff Ondich's 'books.js'
 */

window.addEventListener("load", initialize);

function initialize() {
    loadPerformanceList();

    let element = document.getElementById('ButtonGetData');
    if (element) {
        element.onclick = onAuthorsSelectionChanged;
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

function loadAuthorsSelector() {
    let url = getAPIBaseURL() + '/authors/';

    // Send the request to the books API /authors/ endpoint
    fetch(url, {method: 'get'})

    // When the results come back, transform them from a JSON string into
    // a Javascript object (in this case, a list of author dictionaries).
    .then((response) => response.json())

    // Once you have your list of author dictionaries, use it to build
    // an HTML table displaying the author names and lifespan.
    .then(function(result) {
        // Add the <option> elements to the <select> element
        let selectorBody = '';
        for (let k = 0; k < result.authors.length; k++) {
            let author = result.authors[k];
            selectorBody += '<option value="' + author['id'] + '">'
                                + author['surname'] + ', ' + author['given_name']
                                + '</option>\n';
        }

        let selector = document.getElementById('author_selector');
        if (selector) {
            selector.innerHTML = selectorBody;
        }
    })

    // Log the error if anything went wrong during the fetch.
    .catch(function(error) {
        console.log(error);
    });
}
