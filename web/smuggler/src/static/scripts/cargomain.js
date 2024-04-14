function requestFlag() {
    new Audio('/static/content/flag.mp3').play()
}

function loadTab() {
    // Define the URL of the HTML file corresponding to the tab clicked
    var url = "/" + this.id + "tabdata";

    // Fetch the content from the specified URL
    fetch(url)
        .then(response => {
            // Check if the response is successful (status code 200)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Return the response as text
            return response.text();
        })
        .then(data => {
            // Replace the content of the 'right-column' div with the fetched HTML content
            document.querySelector('.tabcontent').innerHTML = data;
            if(this.id == 'inventory') {
                loadBoxes();
            }
            if(this.id == 'inspection') {
                loadSelection();
                document.getElementById('submitbutton').addEventListener('click', submitReport);
            }
        })
        .catch(error => {
            // Handle any errors that occur during the fetch operation
            console.error('There was a problem with the fetch operation:', error);
        });
}

// This attaches a function to a button. Nice!
document.getElementById("flagbutton").addEventListener('click', requestFlag);

// Hooks for tabs
document.getElementById("about").addEventListener('click', loadTab);
document.getElementById("lawsregs").addEventListener('click', loadTab);
document.getElementById("inventory").addEventListener('click', loadTab);
document.getElementById("inspection").addEventListener('click', loadTab);
// document.getElementById("securityquery").addEventListener('click', loadTab);

// Automatically load about tab at start
document.getElementById('about').click();

let selectedItems = [];
let selectedCargoIDs = [];

// Checkbox functionality
function checkBox(checkbox) {
    var itemId = checkbox.target.closest('.item').querySelector('.checkbox').id;
    // Check if the checkbox is checked
    if (!checkbox.target.checked) {
        // Remove the item id from the list
        let index = selectedItems.indexOf(itemId);
        selectedItems.splice(index, 1);
        selectedCargoIDs.splice(index, 1);
    } else {
        // Add the item id to the list
        selectedItems.push(itemId);
        itemname = document.getElementById(itemId+'b').innerText;
        selectedCargoIDs.push(itemname)
    }
}

function loadDescription(itemname) {
    var itemId = itemname.id;
        // Define the URL of the HTML file corresponding to the tab clicked
    var url = "/" + this.id + "tabdata";
    // Fetch the content from the specified URL
    fetch(url)
        .then(response => {
            // Check if the response is successful (status code 200)
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            // Return the response as text
            return response.text();
        })
        .then(data => {
            // Replace the content of the 'right-column' div with the fetched HTML content
            document.querySelector('.item-content').innerHTML = data;
        })
        .catch(error => {
            // Handle any errors that occur during the fetch operation
            console.error('There was a problem with the fetch operation:', error);
        });
}

function loadBoxes() {
    // Check if selectedItems array is empty

    // If selectedItems array is empty, try to load all the boxes
    const checkboxesquery = document.querySelectorAll('.checkbox');
    const descriptquery = document.querySelectorAll('.item-name');
    console.log(descriptquery)
    checkboxesquery.forEach(function(checkbox) {
        checkbox.addEventListener('click', checkBox);
    });
    descriptquery.forEach(function(itemname) {
        itemname.addEventListener('click', loadDescription);
    });
    // If selectedItems array is not empty, enable checkboxes for each item in the array
    selectedItems.forEach(function(item) {
        const checkbox = document.getElementById(item);
        checkbox.checked = true;
    });

}

function loadSelection() {

    // Loop through the selectedCargoIDs array and create list items
    selectedCargoIDs.forEach(item => {
        // item.parentElement.querySelector('item-name');
        const li = document.createElement("li");
        li.textContent = item;
        selectedItemsList.appendChild(li);
    });

}

function submitReport() {
    fetch("/customsinspection", {
        method: "POST",
        headers: {
            'Content-Type': 'application/json' // Set the content type if sending JSON data
        },
        body: JSON.stringify(selectedCargoIDs)
    })
    //.then(response => response.text()).then(data => result);
    document.getElementById('submitbutton').innerText = "Your response has been recorded.";
    setTimeout(function() { document.getElementById('submitbutton').innerText = "Submit"; }, 2000)
    
}