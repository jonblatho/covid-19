var totalCasesButton = document.getElementById("total-cases");
var newCasesButton = document.getElementById("new-cases");
var activeCasesButton = document.getElementById("active-cases");
var positivityRateButton = document.getElementById("positivity-rate");
var dateMarkersButton = document.getElementById("date-markers");
let selectedClassName = "button-selected";
var activeChartType = 'total';
var prefersDateMarkersOn = true;

function changeChart(type, data) {
    if(type != 'date_markers') {
        totalCasesButton.classList.remove(selectedClassName);
        newCasesButton.classList.remove(selectedClassName);
        activeCasesButton.classList.remove(selectedClassName);
        positivityRateButton.classList.remove(selectedClassName);
    }

    if(type == 'total') {
        totalCasesButton.classList.add(selectedClassName);
    } else if(type == 'new') {
        activeChartType = 'new'
        newCasesButton.classList.add(selectedClassName);
    } else if(type == 'active') {
        activeChartType = 'active'
        activeCasesButton.classList.add(selectedClassName);
    } else if(type == 'pos_rate') {
        activeChartType = 'pos_rate'
        positivityRateButton.classList.add(selectedClassName);
    } else if(type == 'date_markers') {
        if(dateMarkersButton.classList.contains(selectedClassName)) {
            dateMarkersButton.classList.remove(selectedClassName);
        } else {
            dateMarkersButton.classList.add(selectedClassName);
        }
        if(prefersDateMarkersOn == true) {
            prefersDateMarkersOn = false;
            removeDateMarkers();
        } else {
            prefersDateMarkersOn = true;
            addDateMarkers();
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
            maintainAspectRatio: false,
            scales: {
                'x': {
                    type: 'time',
                    min: '2020-04-01',
                    time: {
                        tooltipFormat: 'MMMM D, yyyy',
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

    if(type == 'total' || type == 'new') {
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
                min: '2020-09-04',
                time: {
                    tooltipFormat: 'MMMM D, yyyy',
                    unit: 'month'
                }
            },
            'y': {
                type: 'linear',
                position: 'left',
                min: 0,
                grid: {
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
                grid: {
                    display: true
                }
            }
        };
        chart.options.plugins.tooltip = {
            callbacks: {
                label: function(context) {
                    var label = context.dataset.label || '';

                    if (label) {
                        label += ': ';
                    }
                    if (context.dataset.label == '14-day Positivity Rate') {
                        label += new Intl.NumberFormat('en-US', { style: 'unit', unit: 'percent' }).format(context.parsed.y);
                    } else {
                        label += context.parsed.y;
                    }
                    return label;
                }
            }
        }
    }

    restyleChartForDarkMode();

    if(window.innerWidth > 600) {
        addDateMarkers();
    } else {
        removeDateMarkers();
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
        chart.options.scales['x'].grid.color = 'rgba(255,255,255,0.1)';
        chart.options.scales['y'].grid.color = 'rgba(255,255,255,0.1)';
        chart.options.scales['y'].grid.color = 'rgba(255,255,255,0.1)';
    } else {
        chart.options.scales['x'].grid.color = 'rgba(0,0,0,0.1)';
        chart.options.scales['y'].grid.color = 'rgba(0,0,0,0.1)';
        chart.options.scales['y'].grid.color = 'rgba(0,0,0,0.1)';
        try {
            chart.options.scales['y_tests'].grid.color = 'rgba(0,0,0,0.1)';
            chart.options.scales['y_tests'].grid.color = 'rgba(0,0,0,0.1)';
        } catch { }
    }
}

function reloadChartForTraitChange(trait) {
    if('trait' == 'darkMode') {
        restyleChartForDarkMode();
    }

    chart.update();
}

function addDateMarkers() {
    if(dateMarkersButton.classList.contains(selectedClassName)) {
        dateMarkersButton.classList.add(selectedClassName);
    }
    chart.options.plugins.annotation = markers;

    chart.update();
}

function removeDateMarkers() {
    if(dateMarkersButton.classList.contains(selectedClassName)) {
        dateMarkersButton.classList.remove(selectedClassName);
    }

    chart.options.plugins.annotation = {};
    chart.update();
}