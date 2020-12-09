var totalCasesButton = document.getElementById("total-cases");
var newCasesButton = document.getElementById("new-cases");
var activeCasesButton = document.getElementById("active-cases");
var positivityRateButton = document.getElementById("positivity-rate");
var dateMarkersButton = document.getElementById("date-markers");

function changeChart(type, data) {
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

    if(type != 'date_markers') {
        reloadChart(type, data);
    } else {
        chart.update();
    }
}

function reloadChart(type, data) {
    chart.destroy();

    if(type == 'new') {
        chartType = 'bar';
    } else {
        chartType = 'line';
    }

    chart = new Chart(ctx, {
        type: chartType,
        options: {
            responsive: true,
            aspectRatio: 2.0,
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {
                        tooltipFormat: 'MMMM D, YYYY',
                        unit: 'month'
                    }
                }],
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
        }
    });

    chart.data.labels = chartLabels(type, data);
    chart.data.datasets = chartData(type, data);

    if(type == 'total') {
        chart.options.scales.xAxes[0].stacked = true;
        chart.options.scales.yAxes[0].stacked = true;
        chart.options.plugins = {
            filler: {
                propagate: false
            }
        }
    } else if(type == 'new') {
        chart.options.scales.xAxes[0].stacked = true;
        chart.options.scales.yAxes[0].stacked = true;
        chart.options.plugins = {}
    } else if(type == 'active') {
        chart.options.scales.xAxes[0].stacked = false;
        chart.options.scales.yAxes[0].stacked = false;
    } else if(type == 'pos_rate') {
        chart.options.scales.xAxes[0].stacked = false;
        chart.options.scales.yAxes[0].stacked = false;
    }

    if(type == 'pos_rate') {
        chart.options.scales.yAxes[0].ticks.userCallback = function(value, index, values) {
            value = value.toString();
            value = value.split(/(?=(?:...)*$)/);
            return value + '%';
        }
        chart.options.tooltips.callbacks = {
            label: function(tooltipItem, data) {
                value = tooltipItem.yLabel.toString();
                return '14-day Positivity Rate: ' + value + '%';
            }
        }
    }

    if(dateMarkersButton.classList.contains("chart-selection-selected")) {
        chart.options.annotation = markers
    } else {
        chart.options.annotation = {}
    }

    chart.update()
}