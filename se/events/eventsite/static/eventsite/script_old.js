// script.js
const choicesList = document.getElementById("choices-list");
const displayData = document.getElementById("display-data");

choicesList.addEventListener("change", updateDisplay);

function updateDisplay() {
    const selectedChoices = Array.from(document.querySelectorAll(".choice-checkbox:checked"));
    const selectedChoiceValues = selectedChoices.map(checkbox => checkbox.value);
    
    if (selectedChoiceValues.length === 0) {
        displayData.innerHTML = "No choices selected.";
    } else {
        displayData.innerHTML = "Selected Choices:<br>" + selectedChoiceValues.join("<br>");
    }
}