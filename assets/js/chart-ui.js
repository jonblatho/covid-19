var totalCasesButton = document.getElementById("total-cases");
var newCasesButton = document.getElementById("new-cases");
var activeCasesButton = document.getElementById("active-cases");
var positivityRateButton = document.getElementById("positivity-rate");
var dateMarkersButton = document.getElementById("date-markers");
var yAxisModeButton = document.getElementById("linear-logarithmic");

function changeChart(type, data) {
    let selectedClassName = "button-selected";
    
    if(type != 'date_markers') {
        totalCasesButton.classList.remove(selectedClassName);
        newCasesButton.classList.remove(selectedClassName);
        activeCasesButton.classList.remove(selectedClassName);
        positivityRateButton.classList.remove(selectedClassName);
    }

    if(type == 'total' || type == 'yAxis') {
        totalCasesButton.classList.add(selectedClassName);
    } else if(type == 'new') {
        newCasesButton.classList.add(selectedClassName);
    } else if(type == 'active') {
        activeCasesButton.classList.add(selectedClassName);
    } else if(type == 'pos_rate') {
        positivityRateButton.classList.add(selectedClassName);
    } else if(type == 'date_markers') {
        if(dateMarkersButton.classList.contains(selectedClassName)) {
            dateMarkersButton.classList.remove(selectedClassName);
            dateMarkersButton.innerHTML = "Date Markers";
            chart.options.annotation = {};
        } else {
            dateMarkersButton.classList.add(selectedClassName);
            dateMarkersButton.innerHTML = "Date Markers";
            chart.options.annotation = markers;
        }
    }

    if(type != 'total' && type != 'yAxis') {
        yAxisModeButton.style = 'display: none';
        yAxisModeButton.innerHTML = "Linear"
    } else {
        yAxisModeButton.style = null;

        if(type == 'yAxis') {
            if(yAxisModeButton.innerHTML == "Linear") {
                yAxisModeButton.innerHTML = "Logarithmic"
                chart.options.scales.yAxes[0].type = 'logarithmic'
                chart.options.scales.yAxes[0].ticks.max = 10000
            } else if(yAxisModeButton.innerHTML == "Logarithmic") {
                yAxisModeButton.innerHTML = "Linear"
                chart.options.scales.yAxes[0].type = 'linear'
                chart.options.scales.yAxes[0].ticks.max = chart.options.scales.yAxes[0].ticks.suggestedMax
            }
        }
    }

    if(type != 'date_markers' && type != 'yAxis') {
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
        };
    } else if(type == 'new') {
        chart.options.scales.xAxes[0].stacked = true;
        chart.options.scales.yAxes[0].stacked = true;
        chart.options.plugins = {};
    } else if(type == 'active') {
        chart.options.scales.xAxes[0].stacked = false;
        chart.options.scales.yAxes[0].stacked = false;
    } else if(type == 'pos_rate') {
        chart.options.scales.xAxes[0].stacked = false;
        chart.options.scales.yAxes[0].stacked = false;
    }

    if(type == 'pos_rate') {
        chart.options.scales.yAxes = [
            {
                id: 'pos_rate',
                position: 'left',
                ticks: {
                    beginAtZero: true
                },
                gridLines: {
                    display: true
                }
            },
            {
                id: 'tests',
                position: 'right',
                ticks: {
                    beginAtZero: true,
                    lineWidth: 0
                },
                gridLines: {
                    display: true
                }
            },
        ];
        chart.options.scales.yAxes[0].ticks.userCallback = function(value, index, values) {
            value = value.toString();
            value = value.split(/(?=(?:...)*$)/);
            return value + '%';
        };
        chart.options.tooltips.callbacks = {
            label: function(tooltipItem, data) {
                value = tooltipItem.yLabel.toString();
                if(tooltipItem.datasetIndex == 0) {
                    return '14-day Positivity Rate: ' + value + '%';
                } else if (tooltipItem.datasetIndex == 1) {
                    return '14-day Average Daily Tests: ' + value;
                }
            }
        };
    }

    restyleChartForDarkMode();

    if(dateMarkersButton.classList.contains("button-selected")) {
        chart.options.annotation = markers;
    } else {
        chart.options.annotation = {};
    }

    chart.update();
}

function isDarkMode() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return true;
    }
    return false;
}

function restyleChartForDarkMode() {
    if(isDarkMode()) {
        chart.options.scales.xAxes[0].gridLines.color = 'rgba(255,255,255,0.1)';
        chart.options.scales.yAxes[0].gridLines.color = 'rgba(255,255,255,0.1)';
        try {
            chart.options.scales.xAxes[1].gridLines.color = 'rgba(255,255,255,0.1)';
            chart.options.scales.yAxes[1].gridLines.color = 'rgba(255,255,255,0.1)';
        } catch { }
    } else {
        chart.options.scales.xAxes[0].gridLines.color = 'rgba(0,0,0,0.1)';
        chart.options.scales.yAxes[0].gridLines.color = 'rgba(0,0,0,0.1)';
        try {
            chart.options.scales.xAxes[1].gridLines.color = 'rgba(0,0,0,0.1)';
            chart.options.scales.yAxes[1].gridLines.color = 'rgba(0,0,0,0.1)';
        } catch { }
    }
}

function reloadChartForTraitChange(trait) {
    if('trait' == 'darkMode') {
        restyleChartForDarkMode();
    }

    chart.update();
}