// Functions used for editing page
// Author: Lara Posel (22972221), Joel Phillips (22967051)

function setup() {
    // -------------------------------------------------------------------------------------
    // Create 'Locations' drop down box: 
    // -------------------------------------------------------------------------------------
    
    const locations = ["West Coast Eagles", "UWA Exercise & Performance Centre", "WACRH (Geraldton)", "Agility Rehabilitation", "Curtin Stadium"]; 
    // Which locations must be selected when the page loads (i.e. what the student submitted)
    const selectedLocations = ["West Coast Eagles", "UWA Exercise & Performance Centre", "Agility Rehabilitation"]; 
    
    let locationDropDown = document.createElement("select"); 
    
    for (const location of locations) {
        const choice = document.createElement("option");
        choice.value = location; 
        choice.text = location; 
        locationDropDown.appendChild(choice); 
    }

    locationDropDown.disabled = true; 
    const locationFields = document.getElementsByClassName('location-field'); 

    // Append drop down to each location field table cell: 
    for (let i = 0; i < locationFields.length; i++) {
        const locationDropDownCopy = locationDropDown.cloneNode(true); 
        locationDropDownCopy.value = selectedLocations[i]; 
        locationFields[i].appendChild(locationDropDownCopy); 
    }

    // -------------------------------------------------------------------------------------
    // Create 'supervisors' drop down box: 
    // -------------------------------------------------------------------------------------

    const supervisors = ["Jarryd Heasman", "Joel Young", "Ben Green", "Emma Philipe", "Kane Greenaway"]; 
    const selectedSupervisors = ["Jarryd Heasman", "Joel Young", "Emma Philipe"]; 

    let supervisorDropDown = document.createElement("select"); 
    
    for (const supervisor of supervisors) {
        const choice = document.createElement("option");
        choice.value = supervisor; 
        choice.text = supervisor; 
        supervisorDropDown.appendChild(choice); 
    }

    supervisorDropDown.disabled = true; 
    const supervisorFields = document.getElementsByClassName('supervisor-field'); 

    // Append drop down to each supervisor field table cell: 
    for (let i = 0; i < supervisorFields.length; i++) {
        var supervisorDropDownCopy = supervisorDropDown.cloneNode(true); 
        supervisorDropDownCopy.value = selectedSupervisors[i]; 
        supervisorFields[i].appendChild(supervisorDropDownCopy); 
    }

    // -------------------------------------------------------------------------------------
    // Create 'exercise-prescription' drop down box: 
    // -------------------------------------------------------------------------------------

    const exercisePrescription = ["Exercise Prescription", "Other"]
    const selectedExercisePrescription = ["Exercise Prescription", "Other", "Exercise Prescription"]; 

    let exercisePrescriptionDropDown = document.createElement("select"); 
    
    for (const prescription of exercisePrescription) {
        const choice = document.createElement("option");
        choice.value = prescription; 
        choice.text = prescription; 
        exercisePrescriptionDropDown.appendChild(choice); 
    }

    exercisePrescriptionDropDown.disabled = true; 
    const exercisePrescriptionFields = document.getElementsByClassName('exercise-prescription-field'); 

    // Append drop down to each exercise prescription field table cell: 
    for (let i = 0; i < exercisePrescriptionFields.length; i++) {
        var exercisePrescriptionDropDownCopy = exercisePrescriptionDropDown.cloneNode(true); 
        exercisePrescriptionDropDownCopy.value = selectedExercisePrescription[i]; 
        exercisePrescriptionFields[i].appendChild(exercisePrescriptionDropDownCopy); 
    }

    // -------------------------------------------------------------------------------------
    // Create 'domain' drop down box: 
    // -------------------------------------------------------------------------------------

    const domains = ["Health & Fitness", "Sport & Performance", "Healthy Aging", "Paediatrics & Young People", "Mental Health & Wellness"] 
    const selectedDomains = ["Health & Fitness", "Sport & Performance", "Mental Health & Wellness"]; 

    let domainsDropDown = document.createElement("select"); 
    
    for (const domain of domains) {
        const choice = document.createElement("option");
        choice.value = domain; 
        choice.text = domain; 
        domainsDropDown.appendChild(choice); 
    }

    domainsDropDown.disabled = true; 
    const domainsFields = document.getElementsByClassName('domain-field'); 

    // Append drop down to each domain field table cell: 
    for (let i = 0; i < domainsFields.length; i++) {
        var domainsDropDownCopy = domainsDropDown.cloneNode(true); 
        domainsDropDownCopy.value = selectedDomains[i]; 
        domainsFields[i].appendChild(domainsDropDownCopy); 
    }

    // -------------------------------------------------------------------------------------
    // Add event listeners to all drop downs to enable/disable editing
    // -------------------------------------------------------------------------------------

    const allSelects = document.getElementsByClassName('select');
    for (const tableData of allSelects) { 
        tableData.addEventListener('dblclick', function(event) { 
            const dropDown = this.firstElementChild; 
            dropDown.removeAttribute("disabled");
        });

        tableData.addEventListener('change', function() { 
            const dropDown = this.firstElementChild; 
            dropDown.removeAttribute("disabled");
            this.style.backgroundColor = 'rgb(220, 227, 255)'; 
            dropDown.style.backgroundColor = 'rgb(220, 227, 255)'; 
        });

        tableData.addEventListener('mouseout', function() { 
            const dropDown = this.firstElementChild; 
            dropDown.removeAttribute("disabled");
        });
    }

    const minutesFields = document.getElementsByClassName('text-field'); 
    const initialMinutes = []; 

    for (let i = 0; i < minutesFields.length; i++) { 
        initialMinutes.push(minutesFields[i].innerText); 

        minutesFields[i].addEventListener('dblclick', function() { 
            this.contentEditable = 'true'; 
            this.focus(); 
            this.style.backgroundColor = '#ffcccc'; 
            this.style.color = 'black'; 
        });

        minutesFields[i].addEventListener('blur', function() { 
            this.contentEditable = 'false'; 
            this.style.backgroundColor = ''; 
            this.style.color = 'rgb(165, 164, 164)'; 
            if (validateInput(this.innerText)) {
                this.style.color = "red";
            } else {
                if (this.innerText != initialMinutes[i]) 
                    this.style.backgroundColor = 'rgb(220, 227, 255)'; 
            }
        });

        minutesFields[i].addEventListener('keypress', function(event) { 
            if (event.key == "Enter") { 
                this.contentEditable = 'false'; 
                this.style.backgroundColor = ''; 
                if (this.innerText != initialMinutes[i]) 
                    this.style.backgroundColor = 'rgb(220, 227, 255)'; 
            } 
        });
        
    }
}

// -------------------------------------------------------------------------------------
// Event listeners to edit text fields (only minutes for now, still need to add date editing) 
// -------------------------------------------------------------------------------------
function validateInput(value) { 
    const number = Number(value); 
    if (!(Number.isInteger(number))) {
        alert("Please enter a positive integer in the minutes field."); 
        return true; 
    } else { 
        return false; 
    }
}

/**
 * Submits update for a given row.
 * @param {number} id id of row
 */
function submitUpdate(id) {
    // make object
    const gameObj = {
        logid: id,
        studentid: studentid,
        locationid: 0,
        supervisorid: 0,
        activityid: 0,
        domainid: 0,
        minutes_spent: 0,
        record_date: "",
        unitid: 0
    };

    fetch("/reports/submit_edit", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(gameObj)
    });
    // TODO: reload page afterwards?
}

setup();
