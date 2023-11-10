// script.js
const choicesList = document.getElementById("choices-list");
const displayData = document.getElementById("display-data");
const dateFrom = document.getElementById("from-date");
const dateTo = document.getElementById("to-date");

$(document).ready(function() {
    // Function to update data based on checkbox selections
    function updateDataFromDB() {
        // Create an array to store the selected choices
        var selectedChoices = [];
        var selectedNeighborhood = [];
        
        // Loop through the checkboxes and add selected choices to the array
        $('.choice-checkbox:checked').each(function() {
            selectedChoices.push($(this).val());
        });
        
        $('.neighborhood-checkbox:checked').each(function() {
            selectedNeighborhood.push($(this).val());
        });

        var fromDate = document.getElementById("from-date").value;
        var toDate = document.getElementById("to-date").value;

        var thisWeek = document.getElementById("this-week-checkbox").checked;
        var thisWeekend = document.getElementById("this-weekend-checkbox").checked;

        console.log('week data')

        console.log(thisWeek)
        console.log(thisWeekend)

        console.log('dates')

        console.log(fromDate)
        console.log(toDate)

        // Send an AJAX request to the server to fetch data based on selected choices
        $.ajax({
            url: '/update_data/',  // Replace with the actual URL of your view
            method: 'GET',
            data: {'selected_choices': selectedChoices,
                   'neighborhood_choices': selectedNeighborhood,
                   'fromDate': fromDate,
                   'toDate': toDate,
                   'this_week': thisWeek,
                   'this_weekend': thisWeekend},
            success: function(data) {
                // Update the data displayed from the database
                var newData = '<h2>Events</h2>' + data.data;
                $('#display-data')[0].innerHTML = newData;

            },
            error: function(error) {
                console.error(error);
            }
        });
    }

    // Listen for changes in checkbox selections
    $('.choice-checkbox').on('change', function() {
        updateDataFromDB();
    });

    // Listen for changes in checkbox selections
    $('.neighborhood-checkbox').on('change', function() {
        updateDataFromDB();
    });

    // // Listen for changes in the "From Date" and "To Date" input fields
    $('#from-date, #to-date, #this-week-checkbox, #this-weekend-checkbox').on('change', function() {
        updateDataFromDB();
    });

    document.addEventListener('DOMContentLoaded', function() {
        const addEventBtn = document.getElementById('addEventBtn');
        const eventModal = document.getElementById('eventModal');
        const closeBtn = document.querySelector('.close');
    
        addEventBtn.addEventListener('click', function() {
            eventModal.style.display = 'block';
        });
    
        closeBtn.addEventListener('click', function() {
            eventModal.style.display = 'none';
        });
    
        window.addEventListener('click', function(event) {
            if (event.target === eventModal) {
                eventModal.style.display = 'none';
            }
        });
    
        const eventForm = document.getElementById('eventForm');
    
        eventForm.addEventListener('submit', function(event) {
            event.preventDefault();
    
            // Add your code to handle form submission (e.g., validation, data processing)
    
            // Close the modal after handling the form
            eventModal.style.display = 'none';
        });
    });

});