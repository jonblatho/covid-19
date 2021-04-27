var chevron = document.getElementById("chevron");
var dropdownButton = document.getElementById("dropdown-selected");
var dropdownMenu = document.getElementById("dropdown-menu");
var selectedChartName = document.getElementById("selected-chart-name");
var totalCasesButton = document.getElementById("total-cases");
var newCasesButton = document.getElementById("new-cases");
var activeCasesButton = document.getElementById("active-cases");
var positivityRateButton = document.getElementById("positivity-rate");
var dateMarkersButton = document.getElementById("date-markers");
let selectedClassName = "dropdown-item-selected";
var activeChartType = 'total';
var prefersDateMarkersOn = true;

function showDropdownMenu() {
    if(dropdownMenu.classList.contains("hidden")) {
        dropdownButton.classList.add("dropdown-selected-active")
        dropdownMenu.classList.remove("hidden")
    } else {
        dropdownButton.classList.remove("dropdown-selected-active")
        dropdownMenu.classList.add("hidden")
    }
}

function changeChart(type, data) {
    if(type != 'date_markers') {
        totalCasesButton.classList.remove(selectedClassName);
        newCasesButton.classList.remove(selectedClassName);
        activeCasesButton.classList.remove(selectedClassName);
        positivityRateButton.classList.remove(selectedClassName);
    }

    if(type == 'total') {
        selectedChartName.innerHTML = 'Total Cases'
        totalCasesButton.classList.add(selectedClassName);
    } else if(type == 'new') {
        activeChartType = 'new'
        selectedChartName.innerHTML = 'New Cases'
        newCasesButton.classList.add(selectedClassName);
    } else if(type == 'active') {
        activeChartType = 'active'
        selectedChartName.innerHTML = 'Active Cases'
        activeCasesButton.classList.add(selectedClassName);
    } else if(type == 'pos_rate') {
        activeChartType = 'pos_rate'
        selectedChartName.innerHTML = 'Testing'
        positivityRateButton.classList.add(selectedClassName);
    } else if(type == 'date_markers') {
        if(dateMarkersButton.classList.contains("button-selected")) {
            dateMarkersButton.classList.remove("button-selected");
        } else {
            dateMarkersButton.classList.add("button-selected");
        }
        if(prefersDateMarkersOn == true) {
            prefersDateMarkersOn = false;
            removeDateMarkers();
        } else {
            prefersDateMarkersOn = true;
            addDateMarkers();
        }
    }

    if(!dropdownMenu.classList.contains("hidden")) {
        showDropdownMenu()
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
                    max: end_date,
                    time: {
                        tooltipFormat: 'ddd. MMMM D, yyyy',
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
                    min: 0,
                    grid: {
                        display: false
                    }
                }
            },
            grid: {
                offset: true
            },
            plugins: {
                annotation: markers
            },
            interaction: {
                mode: 'index',
                intersect: false
            },
            animation: false
        }
    });

    chart.data.labels = chartLabels(type, data);
    chart.data.datasets = chartData(type, data);

    if(type == 'total' || type == 'new') {
        chart.options.scales['x'].stacked = true;
        chart.options.scales['y'].stacked = true;
        chart.options.plugins.tooltip.callbacks.afterBody = function(context) {
            filteredContextItems = context.filter(contextItem => contextItem.dataset.label != '7-day Average');
            values = filteredContextItems.map(contextItem => contextItem["raw"]);
            return 'Total: ' + Intl.NumberFormat().format(values.reduce(function(a, b) {
                return a+b;
            }));
        }
    } else if(type == 'active' || type == 'pos_rate') {
        chart.options.scales['x'].stacked = false;
        chart.options.scales['y'].stacked = false;
        chart.options.plugins.tooltip.callbacks.afterBody = function(context) {
            return null;
        }
    }

    if(type == 'pos_rate') {
        chart.options.scales = {
            'x': {
                type: 'time',
                min: '2020-09-02',
                max: end_date,
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
                    display: true,
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
                    display: true,
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

    chart.options.scales['x'].grid.offset = false
    chart.options.scales['x'].grid.color = 'rgba(128,128,128,0.5)';
    chart.options.scales['x'].grid.borderColor = 'rgba(128,128,128,0.5)';
    chart.options.scales['y'].grid.color = 'rgba(128,128,128,0.5)';
    chart.options.scales['y'].grid.borderColor = 'rgba(128,128,128,0.5)';
    chart.options.scales['y_tests'].grid.display = false;

    if(window.innerWidth > 600 && prefersDateMarkersOn == true) {
        addDateMarkers();
    } else {
        removeDateMarkers();
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