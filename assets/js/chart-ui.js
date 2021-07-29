var chevron = document.getElementById("chevron");
var dropdownButton = document.getElementById("dropdown-selected");
var dropdownMenu = document.getElementById("dropdown-menu");
var selectedChartName = document.getElementById("selected-chart-name");
var newCasesButton = document.getElementById("new-cases");
var riskLevelButton = document.getElementById("risk-level-chart");
var totalCasesButton = document.getElementById("total-cases");
var activeCasesButton = document.getElementById("active-cases");
var positivityRateButton = document.getElementById("positivity-rate");
var vaccineDosesButton = document.getElementById("vaccine-doses");
var vaccineResidentsButton = document.getElementById("vaccine-residents");
var dateMarkersButton = document.getElementById("date-markers");
let selectedClassName = "dropdown-item-selected";
var activeChartType = 'new';
var prefersDateMarkersOn = false;

// Set up gradient for Risk Level chart
let width, height, riskLevelGradient;
function riskLevelGradientColor(ctx, chartArea) {
    const chartWidth = chartArea.right - chartArea.left;
    const chartHeight = chartArea.bottom - chartArea.top;
    if (riskLevelGradient === null || width !== chartWidth || height !== chartHeight) {
        // Create the gradient because this is either the first render
        // or the size of the chart has changed
        width = chartWidth;
        height = chartHeight;
        const minScaleValue = chart.scales.y.min;
        const maxScaleValue = chart.scales.y.max;
        if(maxScaleValue == 1.0) {
            return null;
        }
        const scaleRange = maxScaleValue - minScaleValue;
        const lowCutoff = 0.0 / scaleRange;
        const mediumCutoff = 1.0 / scaleRange;
        const highCutoff = 10.0 / scaleRange;
        const criticalCutoff = 25.0 / scaleRange;
        const extremeCutoff = 75.0 / scaleRange;
        console.log(lowCutoff, mediumCutoff, highCutoff, criticalCutoff, extremeCutoff)
        riskLevelGradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
        riskLevelGradient.addColorStop(lowCutoff, '#43B02A');
        riskLevelGradient.addColorStop(mediumCutoff-0.00001, '#43B02A');
        riskLevelGradient.addColorStop(mediumCutoff, '#E0A526');
        riskLevelGradient.addColorStop(highCutoff, '#E0A526');
        riskLevelGradient.addColorStop(highCutoff, '#DC3513');
        riskLevelGradient.addColorStop(criticalCutoff-0.00001, '#DC3513');
        riskLevelGradient.addColorStop(criticalCutoff, '#8A2B2B');
        riskLevelGradient.addColorStop(extremeCutoff-0.00001, '#8A2B2B');
        riskLevelGradient.addColorStop(extremeCutoff, '#DF1995');
    }
    
    return riskLevelGradient;    
}

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
        riskLevelButton.classList.remove(selectedClassName);
        activeCasesButton.classList.remove(selectedClassName);
        positivityRateButton.classList.remove(selectedClassName);
        vaccineDosesButton.classList.remove(selectedClassName);
        vaccineResidentsButton.classList.remove(selectedClassName);
    }

    if(type == 'total') {
        selectedChartName.innerHTML = 'Total Cases'
        totalCasesButton.classList.add(selectedClassName);
    } else if(type == 'new') {
        activeChartType = 'new'
        selectedChartName.innerHTML = 'New Cases'
        newCasesButton.classList.add(selectedClassName);
    } else if(type == 'risk_level') {
        activeChartType = 'risk_level'
        selectedChartName.innerHTML = 'Risk Level'
        riskLevelButton.classList.add(selectedClassName);
    } else if(type == 'active') {
        activeChartType = 'active'
        selectedChartName.innerHTML = 'Active Cases'
        activeCasesButton.classList.add(selectedClassName);
    } else if(type == 'pos_rate') {
        activeChartType = 'pos_rate'
        selectedChartName.innerHTML = 'Testing'
        positivityRateButton.classList.add(selectedClassName);
    } else if(type == 'vaccine_doses') {
        activeChartType = 'vaccine_doses'
        selectedChartName.innerHTML = 'Vaccine Doses'
        vaccineDosesButton.classList.add(selectedClassName);
    } else if(type == 'vaccine_residents') {
        activeChartType = 'vaccine_residents'
        selectedChartName.innerHTML = 'Vaccinated Residents'
        vaccineResidentsButton.classList.add(selectedClassName);
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
    } else if(type == 'risk_level' || type == 'active' || type == 'pos_rate') {
        chart.options.scales['x'].stacked = false;
        chart.options.scales['y'].stacked = false;
        if(type == 'risk_level') {
            chart.data.datasets[0].borderColor = function(context) {
                const chartObject = context.chart;
                const {ctx, chartArea} = chartObject;
                if (!chartArea) {
                    // This case happens on initial chart load
                    return null;
                }
                return riskLevelGradientColor(ctx, chartArea);
            }
        }
        chart.options.plugins.tooltip.callbacks.afterBody = function(context) {
            if(type == 'risk_level') {
                value = context[0].raw
                if(value < 1) {
                    return 'Low Risk';
                } else if(value < 10) {
                    return 'Medium Risk'
                } else if(value < 25) {
                    return 'High Risk'
                } else if(value < 75) {
                    return 'Critical Risk'
                } else {
                    return 'Extreme Risk';
                }
            } else {
                return null;
            }
        }
    } else if(type == 'vaccine_doses' || type == 'vaccine_residents') {
        console.log("Setting minimum x-axis value to 2020-12-15.")
        chart.options.scales = {
            'x': {
                type: 'time',
                min: '2020-12-15',
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
                }
            },
            'y_tests': {
                type: 'linear',
                position: 'right',
                min: 0,
                display: false
            }
        }
    }

    if(type == 'pos_rate') {
        chart.options.scales = {
            'x': {
                type: 'time',
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