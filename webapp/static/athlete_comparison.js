let base;

document.addEventListener("DOMContentLoaded", function () {
  const toggleBtn = document.getElementById("col1_2Toggle");
  const comparison2 = document.getElementById("Comparison2");q

  if (toggleBtn && comparison2) {
    toggleBtn.addEventListener("click", function () {
      const isShown = comparison2.classList.toggle("shown");
      toggleBtn.textContent = isShown
        ? "Hide Second Athlete Page"
        : "Show Second Athlete Page";
    });
  }
});




window.addEventListener("load", initialize);

function initialize() {
    let container = document.getElementById('athleteList');
    let athletes = container.querySelectorAll('div');
    const container1   = document.getElementById('Comparison1');
     base  = container1.innerHTML;     
    athletes.forEach(div => {
        div.addEventListener('click', () => {
            let id = div.getAttribute('data-id')
            displayAthlete(id)
        })
    })


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

function displayAthlete(id) {
    let cmp = document.getElementById('Comparison1');
    cmp.innerHTML = '<p>Loading…</p>';

    let url = getAPIBaseURL() + '/athlete/';
    if(id) url += id;

    fetch(url, {method: 'get'})
    .then(response => response.json())
    .then(function(athlete) {
        if (!athlete || !athlete.event_name) {
          console.log('No athlete data found:', athlete);
            cmp.innerHTML = '<button id="backBtn" class="btn btn-secondary mb-3">⬅ Back</button> <p>No data found for this athlete.</p>';
            document.getElementById('backBtn').addEventListener('click', () => {
              cmp.innerHTML = base;
              initialize(); 
          });
            
            return;
        }

        let html = '<button id="backBtn" class="btn btn-secondary mb-3">⬅ Back</button>';
        html += `
            <div class="row mb-4">
                <div class="col"><h4>Name:</h4> ${athlete.first_name} ${athlete.last_name}</div>
                <div class="col"><h5>Gender:</h5> ${athlete.gender}</div>
                <div class="col"><h5>School:</h5> ${athlete.school}</div>
            </div>
        `;

        Object.entries(athlete.event_name).forEach(([event, eventData]) => {
            html += `
                <h5>${event} <small class="text-muted">(${eventData.event_category})</small></h5>
                <table class="table table-striped table-bordered mb-4">
                    <thead class="table-dark">
                        <tr>
                            <th>Mark</th>
                            <th>Meet</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            eventData.performances.forEach(performance => {
                html += `
                    <tr>
                        <td>${performance.mark}</td>
                        <td>${performance.meet}</td>
                        <td>${performance.date}</td>
                    </tr>
                `;
            });

            html += `
                    </tbody>
                </table>
            `;
        });

        cmp.innerHTML = html;

        document.getElementById('backBtn').addEventListener('click', () => {
            cmp.innerHTML = base; 
            initialize(); 
          });

    })
    .catch(function(error) {
        console.log(error);
        cmp.innerHTML = '<p>Error loading athlete data.</p>';
    });
}


