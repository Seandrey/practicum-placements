document.getElementById('studentReport').style.display = 'none'; 

function submitSearch() { 
    var name = document.getElementById('studentSearch').value; 
    document.getElementById('reportTitle').innerHTML = "Practical Hours: " + name; 
    document.getElementById('studentSearch').value = ""; 
    document.getElementById('studentReport').style.display = 'block'; 
    // document.getElementById('listOfNames').style.display = "none"; 
    document.getElementById('listOfNames').style.visibility = "hidden"; 
    document.getElementById("caret").removeAttribute("class","fa fa-caret-left"); 
    document.getElementById("caret").setAttribute("class", "fa fa-caret-down");
}

document.getElementById('studentSearch').addEventListener("keypress", function(event) { 
    if (event.key == "Enter") {
        submitSearch()
    }
}); 

var allNames = document.getElementById('listOfNames').childNodes; 

for (let i=0; i<allNames.length; i++) { 
    allNames[i].addEventListener("click", function() {
        var name = this.innerText; 
        document.getElementById('reportTitle').innerHTML = "Practical Hours: " + name; 
        document.getElementById('studentSearch').value = ""; 
        document.getElementById('studentReport').style.display = 'block'; 
        // document.getElementById('listOfNames').style.display = "none"; 
        document.getElementById('listOfNames').style.visibility = "hidden"; 
        document.getElementById("caret").removeAttribute("class","fa fa-caret-left"); 
        document.getElementById("caret").setAttribute("class", "fa fa-caret-down");
        }
    )
}

document.getElementById('studentSearch').addEventListener("click", function() { 
    // document.getElementById('listOfNames').style.display = "inline-block"; 
    if (document.getElementById('listOfNames').style.visibility == "visible") {
        document.getElementById('listOfNames').style.visibility = "hidden"; 
        document.getElementById("caret").removeAttribute("class","fa fa-caret-left"); 
        document.getElementById("caret").setAttribute("class", "fa fa-caret-down"); }
    else { 
        document.getElementById('listOfNames').style.visibility = "visible";
        document.getElementById("caret").removeAttribute("class","fa fa-caret-down"); 
        document.getElementById("caret").setAttribute("class", "fa fa-caret-left"); 
    }
} )

document.getElementById("caretButton").addEventListener("click", function() { 
    if (document.getElementById('listOfNames').style.visibility == "visible") {
        document.getElementById('listOfNames').style.visibility = "hidden";
        document.getElementById("caret").removeAttribute("class","fa fa-caret-left"); 
        document.getElementById("caret").setAttribute("class", "fa fa-caret-down"); 
    }
    else { 
        document.getElementById('listOfNames').style.visibility = "visible";
        document.getElementById("caret").removeAttribute("class","fa fa-caret-down"); 
        document.getElementById("caret").setAttribute("class", "fa fa-caret-left"); 
    }

    
})

// document.getElementById('searchMenu').addEventListener("blur", function() { 
//     // document.getElementById('listOfNames').style.display = "none"; 
//     document.getElementById('listOfNames').style.visibility = "hidden"; 
// } )

// document.getElementById('dropDown').addEventListener("mouseout", function() { 
//     // document.getElementById('listOfNames').style.display = "none"; 
//     document.getElementById('listOfNames').style.visibility = "hidden"; 
// } )


document.getElementById('searchButton').addEventListener("click", submitSearch); 


function hideElements() { 
    document.getElementById('sidebar').style.display = 'none'; 
    document.getElementById('studentReportInfo').style.display = 'none'; 
    document.getElementById('rightBlock').style.width = "100%"; 
    document.getElementById('rightBlock').style.margin = "0%"; 
    document.getElementById('rightBlock').style.backgroundColor = "white"; 
    document.getElementsByTagName('body')[0].style.backgroundColor = "white"; 
}


var reportButton = document.getElementById('createReport');
reportButton.addEventListener("click", hideElements);  



