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
            // chart.options.annotation = {};
        } else {
            dateMarkersButton.classList.add(selectedClassName);
            dateMarkersButton.innerHTML = "Date Markers";
            // chart.options.annotation = markers;
        }
    }

    if(type != 'total' && type != 'yAxis' && type != 'date_markers') {
        yAxisModeButton.style = 'display: none';
        yAxisModeButton.innerHTML = "Linear"
    } else if(type != 'date_markers') {
        yAxisModeButton.style = null;

        if(type == 'yAxis') {
            if(yAxisModeButton.innerHTML == "Linear") {
                yAxisModeButton.innerHTML = "Logarithmic"
                chart.options.scales['y'].type = 'logarithmic'
                chart.options.scales['y'].max = 10000
            } else if(yAxisModeButton.innerHTML == "Logarithmic") {
                yAxisModeButton.innerHTML = "Linear"
                chart.options.scales['y'].type = 'linear'
                chart.options.scales['y'].max = chart.options.scales['y'].suggestedMax
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
                'x': {
                    type: 'time',
                    time: {
                        tooltipFormat: 'MMMM d, yyyy',
                        unit: 'month'
                    }
                },
                'y': {
                    min: 0,
                    display: 'auto',
                },
                'y_tests': {
                    position: 'right',
                    display: 'auto',
                    min: 0
                }
            },
            plugins: {
                annotation: markers
            },
            interaction: {
                mode: 'index',
                intersect: false
            }
        }
    });

    chart.data.labels = chartLabels(type, data);
    chart.data.datasets = chartData(type, data);

    if(type == 'total') {
        chart.options.scales['x'].stacked = true;
        chart.options.scales['y'].stacked = true;
    } else if(type == 'new') {
        chart.options.scales['x'].stacked = true;
        chart.options.scales['y'].stacked = true;
    } else if(type == 'active' || type == 'pos_rate') {
        chart.options.scales['x'].stacked = false;
        chart.options.scales['y'].stacked = false;
    }

    if(type == 'pos_rate') {
        chart.options.scales = {
            'x': {
                type: 'time',
                time: {
                    tooltipFormat: 'MMMM d, yyyy',
                    unit: 'month'
                }
            },
            'y': {
                type: 'linear',
                position: 'left',
                min: 0,
                gridLines: {
                    display: true
                },
                ticks: {
                    callback: function(value, index, values) {
                        value = value.toString();
                        value = value.split(/(?=(?:...)*$)/);
                        return value + '%';
                    }
                }
            },
            'y_tests': {
                type: 'linear',
                position: 'right',
                min: 0,
                gridLines: {
                    display: true
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
        chart.options.scales['y'].gridLines.color = 'rgba(255,255,255,0.1)';
        chart.options.scales['y'].gridLines.color = 'rgba(255,255,255,0.1)';
    } else {
        chart.options.scales['y'].gridLines.color = 'rgba(0,0,0,0.1)';
        chart.options.scales['y'].gridLines.color = 'rgba(0,0,0,0.1)';
        try {
            chart.options.scales['y_tests'].gridLines.color = 'rgba(0,0,0,0.1)';
            chart.options.scales['y_tests'].gridLines.color = 'rgba(0,0,0,0.1)';
        } catch { }
    }
}

function reloadChartForTraitChange(trait) {
    if('trait' == 'darkMode') {
        restyleChartForDarkMode();
    }

    chart.update();
}