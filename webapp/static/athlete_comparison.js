window.addEventListener("load", initialize);
const fixedBtn = document.getElementById("fixedButton");
const container = document.getElementById("container");
// Stores div and necessary data via Map
const contentWrapperState = new Map();


// handles both loading from href (with athleteId), which loads the athlete info into the initial divider and just base loading
function initialize() {
    const firstDivider = createDivider(0);
    firstDivider.classList.remove("divider-enter");
    container.appendChild(firstDivider);

    reorganizeRows();
    setDividerHeights();

    const athleteId = getAthleteIdFromURL();
    if (athleteId) {
        const contentWrapper = firstDivider.querySelector(".content-wrapper");
        const initialSearchFormContainer = firstDivider.querySelector(".search-form-wrapper");

        if (contentWrapper && initialSearchFormContainer) {
            // Save the initial search form state for back navigation
            contentWrapperState.set(contentWrapper, {
                type: 'searchForm',
                content: initialSearchFormContainer
            });

            initialSearchFormContainer.style.display = 'none';
            displayAthlete(athleteId, contentWrapper); // simplified param call thanks to contentWrapper
        }
    }
}

// to handle opening athlete comparison from href (from other pages)
function getAthleteIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('athleteId');
}

window.addEventListener("resize", setDividerHeights);

function getAPIBaseURL() {
  let baseURL =
    window.location.protocol +
    "//" +
    window.location.hostname +
    ":" +
    window.location.port +
    "/api";
  return baseURL;
}


// Main function -- Given an athlete Id and whatever divider the search is queried from, populates that divider with all pertinent athlete info. Also includes a back button to either return to the athlete list or search form, depending on how this is called
function displayAthlete(id, contentWrapper) {
    if (!contentWrapper) return;

    contentWrapper.innerHTML = "<p>Loading…</p>";

    const url = `${getAPIBaseURL()}/athlete/${id}`;

    fetch(url)
        .then((response) => response.json())
        .then((athlete) => {
            const dynamicBackBtn = document.createElement("button");
            dynamicBackBtn.type = "button";
            dynamicBackBtn.className = "circle-btn back-btn";
            dynamicBackBtn.innerHTML = `<i class="bi bi-arrow-left"></i>`;

            dynamicBackBtn.addEventListener("click", () => {
                const previousState = contentWrapperState.get(contentWrapper);

                if (previousState) {
                    contentWrapper.innerHTML = ""; // Clear current athlete display

                    //show previous Form, either search form or athlete list w/ back button
                    if (previousState.type === 'searchForm') {
                        previousState.content.style.display = 'block'; 
                        contentWrapper.appendChild(previousState.content);
                    } else if (previousState.type === 'athleteList') {
                        contentWrapper.appendChild(previousState.content); 
                        contentWrapper.appendChild(previousState.backButton); 
                    }
                } else {
                    console.warn("Back button clicked, but no previous state to restore.");
                }
            });


            if (!athlete || !athlete.event_name) {
                console.log("No athlete data found:", athlete);
                contentWrapper.innerHTML = `
                    <div class="w-100">
                        <p>No data found for this athlete.</p>
                    </div>
                `;
                contentWrapper.prepend(dynamicBackBtn);
                return;
            }

            const wrapper = document.createElement("div");
            wrapper.className = "w-100";
            wrapper.innerHTML = `
                <div class="row mt-5 mb-4">
                    <div class="col"><h4>Name:</h4> ${athlete.first_name} ${athlete.last_name}</div>
                    <div class="col"><h5>Gender:</h5> ${athlete.gender}</div>
                    <div class="col"><h5>School:</h5> ${athlete.school}</div>
                </div>
            `;

            // Sort the events before populating tables
            Object.entries(athlete.event_name)
                .sort(([eventA], [eventB]) => eventA.localeCompare(eventB))
                .forEach(([event, eventData]) => {
                    const eventBlock = document.createElement("div");
                    eventBlock.className = "mb-5";

                    let tableHTML = `
                        <h5>${event} <small class="text-muted">(${eventData.event_category})</small></h5>
                        <div class="table-responsive">
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
                    eventData.performances.forEach((performance) => {
                        tableHTML += `
                            <tr>
                                <td>${performance.mark}</td>
                                <td>${performance.meet}</td>
                                <td>${performance.date}</td>
                            </tr>
                        `;
                    });

                    tableHTML += `</tbody></table></div>`;
                    eventBlock.innerHTML = tableHTML;
                    wrapper.appendChild(eventBlock);
                });

            contentWrapper.innerHTML = "";
            contentWrapper.appendChild(wrapper);
            wrapper.prepend(dynamicBackBtn);

        })
        .catch((error) => {
            console.error("Error fetching athlete:", error);
            contentWrapper.innerHTML = "<p class='text-danger'>Error loading athlete data.</p>";
            const errorBackBtn = document.createElement("button");
            errorBackBtn.type = "button";
            errorBackBtn.className = "circle-btn back-btn";
            errorBackBtn.innerHTML = `<i class="bi bi-arrow-left"></i>`;
            errorBackBtn.addEventListener("click", () => {
                const previousState = contentWrapperState.get(contentWrapper);
                if (previousState && previousState.type === 'searchForm') {
                    contentWrapper.innerHTML = "";
                    previousState.content.style.display = 'block';
                    contentWrapper.appendChild(previousState.content);
                } else {
                    contentWrapper.innerHTML = "<p>Please try again.</p>";
                }
            });
            contentWrapper.prepend(errorBackBtn);
        });
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// Divider add/remove/reorganize functions

function reorganizeRows() {
  // Re organizes rows --- makes it so that all rows have max 2 dividers within them, and if an upper divider is deleted, the others move
  const cols = Array.from(container.querySelectorAll(".divider-col"));
  container.innerHTML = "";

  for (let i = 0; i < cols.length; i += 2) {
    const row = document.createElement("div");
    row.className = "row my-4 d-flex align-items-stretch";

    row.appendChild(cols[i]);
    if (cols[i + 1]) row.appendChild(cols[i + 1]);

    if (row.children.length === 1) {
      cols[i].classList.remove("col-md-6");
      cols[i].classList.add("col");
    } else {
      cols[i].classList.remove("col");
      cols[i].classList.add("col-md-6");
      cols[i + 1].classList.remove("col");
      cols[i + 1].classList.add("col-md-6");
    }

    container.appendChild(row);
  }
}


// Sets the divider heights based on VH and number of dividers (so 4 dividers can be seen on screen without scrolling)
function setDividerHeights() {
  const dividers = container.querySelectorAll(".dark-divider");
  const count = dividers.length;

  if (count <= 2) {
    dividers.forEach((div) => {
      div.style.height = "85vh";
    });
  } else {
    const verticalMargin = 48;
    const extraPadding = 20;
    const availableHeight = window.innerHeight - verticalMargin - extraPadding;
    const dividerHeight = availableHeight / 2;

    dividers.forEach((div) => {
      div.style.height = `${dividerHeight}px`;
    });
  }
}

// Creates a divider with the search form within it
function createDivider(index) {
    const col = document.createElement("div");
    col.className = "col divider-col divider-enter";

    const divider = document.createElement("div");
    divider.className =
        "dark-divider bg-dark text-white text-center position-relative rounded";

    const contentWrapper = document.createElement("div");
    contentWrapper.className =
        "content-wrapper d-flex justify-content-center align-items-start";
    contentWrapper.style.height = "100%";
    contentWrapper.style.overflowY = "auto";

    const searchFormContainer = document.createElement("div");
    searchFormContainer.className =
        "search-form-wrapper bg-body-tertiary p-3 rounded-4 text-start";
    searchFormContainer.style.width = "65%";
    searchFormContainer.style.color = "black";
    searchFormContainer.setAttribute('data-index', index); // Set data-index for selection of divs by their assigned index

    searchFormContainer.innerHTML = `
        <form id="athleteSearchForm_${index}" class="mb-4" method="GET" action="/api/search">
            <h4 class="mb-4">Athlete Search:</h4>

            <div class="row mb-2">
                <div class="col">
                    <label for="nameInput_${index}" class="form-label">Name</label>
                    <input type="text" id="nameInput_${index}" name="name" class="form-control" placeholder="Search By Athlete Name">
                </div>
            </div>

            <hr class="my-4" />
            <h5 class="mb-3">Optional Filtering</h5>

            <div class="row mb-3">
                <div class="col">
                    <label for="eventSelect_${index}" class="form-label">Event</label>
                    <select id="eventSelect_${index}" name="event" class="form-select w-100" style="max-height: 150px; overflow-y: auto;"></select>
                </div>
            </div>

            <div class="row">
                <div class="col d-flex align-items-center">
                    <fieldset class="border-0">
                        <legend class="col-form-label pt-0">Gender</legend>
                        <div class="form-check form-check-inline">
                            <input type="radio" name="gender_${index}" class="form-check-input" id="genderNone_${index}" value="" checked />
                            <label class="form-check-label" for="genderNone_${index}">Any</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input type="radio" name="gender_${index}" class="form-check-input" id="genderMen_${index}" value="m" />
                            <label class="form-check-label" for="genderMen_${index}">Men</label>
                        </div>
                        <div class="form-check form-check-inline">
                            <input type="radio" name="gender_${index}" class="form-check-input" id="genderWomen_${index}" value="f" />
                            <label class="form-check-label" for="genderWomen_${index}">Women</label>
                        </div>
                    </fieldset>
                </div>
            </div>

            <div class="row">
                <div class="col">
                    <label for="teamSelect_${index}" class="form-label d-block">Teams</label>
                    <select id="teamSelect_${index}" name="team" class="form-select w-100"></select>
                </div>
            </div>

            <div class="row mb-5">
                <div class="col align-items-center">
                    <label for="seasonSelect_${index}" class="form-label">Season</label>
                    <select id="seasonSelect_${index}" name="season" class="form-select w-100"></select>
                </div>
            </div>
            <div class="d-grid">
                <button id="athleteSearchButton_${index}" type="submit" class="btn btn-primary btn-lg">Search</button>
            </div>
        </form>
    `;

    const closeBtn = document.createElement("button");
    closeBtn.type = "button";
    closeBtn.className = "circle-btn close-btn";
    closeBtn.setAttribute("aria-label", "Close divider");
    closeBtn.innerHTML = `<i class="bi bi-x-lg"></i>`;

    closeBtn.addEventListener("click", () => removeDivider(col));

    contentWrapper.appendChild(searchFormContainer);
    divider.appendChild(closeBtn);
    divider.appendChild(contentWrapper);
    col.appendChild(divider);

    // These functions pull the index from the container and load the searchForm with pertinent data
    loadEventsSelector(searchFormContainer);
    loadSeasonsSelector(searchFormContainer);
    loadTeamsSelector(searchFormContainer);

    // Calls searchSubmit function when form search is pressed
    const form = searchFormContainer.querySelector(`#athleteSearchForm_${index}`);
    if (form) {
        form.addEventListener("submit", (event) => {
            handleAthleteSearchSubmit(event, contentWrapper, searchFormContainer); // Removed index param from here
        });
    }

    contentWrapperState.set(contentWrapper, {
        type: 'searchForm',
        content: searchFormContainer
    });

    return col;
}

// Removes divider and reorganizes rows
function removeDivider(col) {
    const contentWrapper = col.querySelector(".content-wrapper");
    if (contentWrapper) {
        contentWrapperState.delete(contentWrapper);
    }

    col.classList.add("divider-leave");
    requestAnimationFrame(() => {
        col.classList.add("divider-leave-active");
        col.addEventListener(
            "transitionend",
            () => {
                col.remove();
                reorganizeRows();
                setDividerHeights();
            }, {
                once: true
            }
        );
    });
}


fixedBtn.addEventListener("click", () => {
  const currentCount = container.querySelectorAll(".divider-col").length;
  if (currentCount >= 4) return;

  const newDivider = createDivider(currentCount);
  container.appendChild(newDivider);

  reorganizeRows();
  setDividerHeights();

  requestAnimationFrame(() => {
    newDivider.classList.add("divider-enter-active");
    newDivider.classList.remove("divider-enter");
  });
});


////////////////////////////////////////////////////////////////////////////////////////////////////

// athleteSearchForm Functions


// Handles athlete name search within divider
async function handleAthleteSearchSubmit(event, contentWrapper, searchFormContainer) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    const index = searchFormContainer.getAttribute('data-index'); // Get index from data attribute of div

    const data = {
        nameInput: formData.get("name") || "",
        event: formData.get("event") || "",
        gender: formData.get(`gender_${index}`) || "",
        team: formData.get("team") || "",
        season: formData.get("season") || ""
    };

    localStorage.setItem(`athleteSearchForm_${index}`, JSON.stringify(data));
    console.log("Saved athlete search form data for divider", index, data);

    contentWrapper.innerHTML = "<p>Searching…</p>";
    searchFormContainer.style.display = 'none';

    try {
        const queryParams = new URLSearchParams();
        if (data.nameInput) queryParams.append("nameInput", data.nameInput);
        if (data.event) queryParams.append("event", data.event);
        if (data.gender) queryParams.append("gender", data.gender);
        if (data.team) queryParams.append("team", data.team);
        if (data.season) queryParams.append("season", data.season);

        const response = await fetch(`/api/athleteSearch?${queryParams.toString()}`);
        if (!response.ok) throw new Error("Network response was not ok");

        const result = await response.json();

        if (result.error) {
            contentWrapper.innerHTML = `<p class="text-danger">Error: ${result.error}</p>`;
            addBackToSearchButton(contentWrapper, searchFormContainer);
        } else if (result.athletes && result.athletes.length > 0) {
            displayAthleteSearchResults(result.athletes, contentWrapper, searchFormContainer);
        } else {
            contentWrapper.innerHTML = "<p>No athletes found matching your criteria.</p>";
            addBackToSearchButton(contentWrapper, searchFormContainer);
        }

    } catch (err) {
        console.error("Fetch error:", err);
        alert("An error occurred while searching. Please try again.");
        contentWrapper.innerHTML = "<p class='text-danger'>An error occurred while searching. Please try again.</p>";
        addBackToSearchButton(contentWrapper, searchFormContainer);
    }
}
// Displays the returned list of athletes within each divider
function displayAthleteSearchResults(athletes, contentWrapper, searchFormContainer) {
    contentWrapper.innerHTML = ""; 

    const athleteListDiv = document.createElement("div");
    athleteListDiv.className = "athlete-list p-3 text-white overflow-auto";
    athleteListDiv.innerHTML = `<h5>Search Results (${athletes.length} athletes):</h5>`;

    athletes.forEach(a => {
        const athleteDiv = document.createElement("div");
        athleteDiv.className = "athlete-entry p-2 mb-2 bg-secondary rounded";
        athleteDiv.setAttribute("data-id", a.id);
        athleteDiv.style.cursor = "pointer";

        athleteDiv.innerHTML = `
            <strong>${a.first_name} ${a.last_name}</strong> (${a.gender.toUpperCase()}), School: ${a.school}
        `;

        athleteDiv.addEventListener("click", () => {
            
            contentWrapperState.set(contentWrapper, {
                type: 'athleteList',
                content: athleteListDiv,
                backButton: backBtnForList
            });
            displayAthlete(a.id, contentWrapper);
        });
        athleteListDiv.appendChild(athleteDiv);
    });

    const backBtnForList = document.createElement("button");
    backBtnForList.type = "button";
    backBtnForList.className = "circle-btn back-btn";
    backBtnForList.innerHTML = `<i class="bi bi-arrow-left"></i>`;

    backBtnForList.addEventListener("click", () => {
        contentWrapper.innerHTML = "";
        contentWrapper.appendChild(searchFormContainer);
        searchFormContainer.style.display = 'block';
        contentWrapperState.set(contentWrapper, {
            type: 'searchForm',
            content: searchFormContainer
        });
    });

    contentWrapper.appendChild(athleteListDiv);
    contentWrapper.appendChild(backBtnForList);
}

// Adds back button to displayed list of athletes
function addBackToSearchButton(contentWrapper, searchFormContainer) {
    const backBtn = document.createElement("button");
    backBtn.type = "button";
    backBtn.className = "circle-btn back-btn";
    backBtn.innerHTML = `<i class="bi bi-arrow-left"></i>`;
    backBtn.addEventListener("click", () => {
        contentWrapper.innerHTML = "";
        contentWrapper.appendChild(searchFormContainer);
        searchFormContainer.style.display = 'block';
        // When returning to search form, update the state for this contentWrapper
        contentWrapperState.set(contentWrapper, {
            type: 'searchForm',
            content: searchFormContainer
        });
    });
    contentWrapper.prepend(backBtn);
}



///////////////////////////////////////////////////////////////////////////////////////////

// Functions to populate each search form dropdown via the database

function loadEventsSelector(container) {
    const index = container.getAttribute('data-index');
    let url = getAPIBaseURL() + "/events/";
    fetch(url, {
            method: "get"
        })
        .then((response) => response.json())
        .then(function(result) {
            let selectorBody = '<option value="">-- Select Event (Optional) --</option>\n';
            for (let k = 0; k < result.length; k++) {
                let event = result[k];
                selectorBody +=
                    '<option value="' +
                    event["event_name"] +
                    '">' +
                    event["event_name"] +
                    "</option>\n";
            }
            // Use specific ID from the assigned index
            let selector = container.querySelector(`#eventSelect_${index}`);
            if (selector) {
                selector.innerHTML = selectorBody;
            }
        })
        .catch(function(error) {
            console.log(error);
        });
}

function loadSeasonsSelector(container) {
    const index = container.getAttribute('data-index');
    let url = getAPIBaseURL() + "/seasons/";
    fetch(url, {
            method: "get"
        })
        .then((response) => response.json())
        .then(function(result) {
            let selectorBody = '<option value="">-- Select Season (Optional) --</option>\n';
            for (let k = 0; k < result.length; k++) {
                let season = result[k];
                selectorBody +=
                    '<option value="' +
                    season["season_name"] +
                    '">' +
                    season["season_name"] +
                    "</option>\n";
            }
            // Use specific ID from the index
            let selector = container.querySelector(`#seasonSelect_${index}`);
            if (selector) {
                selector.innerHTML = selectorBody;
            }
        })
        .catch(function(error) {
            console.log(error);
        });
}

async function loadTeamsSelector(container) {
    const index = container.getAttribute('data-index');
    try {
        const response = await fetch(getAPIBaseURL() + "/teams/");
        if (!response.ok) throw new Error("Network response was not OK");

        const teams = await response.json();

        // Use specific ID from the index
        const select = container.querySelector(`#teamSelect_${index}`);
        if (!select) {
            console.error("Team select element not found for index:", index);
            return;
        }

        select.innerHTML = "";

        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.textContent = "-- Select a Team (Optional) --";
        select.appendChild(defaultOption);

        teams.forEach((team) => {
            const option = document.createElement("option");
            option.value = team.school_name;
            option.textContent = team.school_name;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Failed to load teams:", error);
    }
}