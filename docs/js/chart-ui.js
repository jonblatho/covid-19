var totalCasesButton = document.getElementById("total-cases");
var newCasesButton = document.getElementById("new-cases");
var activeCasesButton = document.getElementById("active-cases");
var positivityRateButton = document.getElementById("positivity-rate");
var dateMarkersButton = document.getElementById("date-markers");

function changeChart(type) {
    if(type == 'total') {
        totalCasesButton.classList.add("chart-selection-selected");
        newCasesButton.classList.remove("chart-selection-selected");
        activeCasesButton.classList.remove("chart-selection-selected");
        positivityRateButton.classList.remove("chart-selection-selected");
    } else if(type == 'new') {
        totalCasesButton.classList.remove("chart-selection-selected");
        newCasesButton.classList.add("chart-selection-selected");
        activeCasesButton.classList.remove("chart-selection-selected");
        positivityRateButton.classList.remove("chart-selection-selected");
    } else if(type == 'active') {
        totalCasesButton.classList.remove("chart-selection-selected");
        newCasesButton.classList.remove("chart-selection-selected");
        activeCasesButton.classList.add("chart-selection-selected");
        positivityRateButton.classList.remove("chart-selection-selected");
    } else if(type == 'pos_rate') {
        totalCasesButton.classList.remove("chart-selection-selected");
        newCasesButton.classList.remove("chart-selection-selected");
        activeCasesButton.classList.remove("chart-selection-selected");
        positivityRateButton.classList.add("chart-selection-selected");
    } else if(type == 'date_markers') {
        if(dateMarkersButton.classList.contains("chart-selection-selected")) {
            dateMarkersButton.classList.remove("chart-selection-selected");
            dateMarkersButton.innerHTML = "Date Markers Off"
            chart.options.annotation = {}
        } else {
            dateMarkersButton.classList.add("chart-selection-selected");
            dateMarkersButton.innerHTML = "Date Markers On"
            chart.options.annotation = markers
        }

    }

    reloadChart(type);
}

function reloadChart(type) {
    if(type == 'total') {

    }
    chart.update()
}