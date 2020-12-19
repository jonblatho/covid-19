// Load the data from chart-data/data.json
function loadData(url) {
    if (json == null) {
        fetch(url)
        .then(res => res.json())
        .then((out) => {
            json = out
            reloadChart('total', json);
        })
        .catch(err => { throw err } );
    }
}

function chartLabels(type, data) {
    var dates = data.map(day => day["date"]);

    if(type == 'pos_rate') {
        dates = dates.slice(154);
    }

    return dates
}

function chartData(type, data) {
    if(type == 'total') {
        var sets = [];
        sets.push(data.map(day => day["total_cases"]["west_plains"]));
        sets.push(data.map(day => day["total_cases"]["willow_springs"]));
        sets.push(data.map(day => day["total_cases"]["mountain_view"]));
        sets.push(data.map(day => day["total_cases"]["other"]));
        sets.push(data.map(day => day["total_cases"]["unknown"]));
        datasets = []
        sets.forEach(function(values, index) {
            datasets.push(
                {
                    data: values,
                    label: categories[index],
                    pointRadius: 0,
                    backgroundColor: categoryColors[index]
                }
            )
        });
        return datasets;
    } else if(type == 'new') {
        var sets = [];
        sets.push(data.map(day => day["new_cases"]["west_plains"]));
        sets.push(data.map(day => day["new_cases"]["willow_springs"]));
        sets.push(data.map(day => day["new_cases"]["mountain_view"]));
        sets.push(data.map(day => day["new_cases"]["other"]));
        sets.push(data.map(day => day["new_cases"]["unknown"]));
        datasets = []
        // Add data by town
        sets.forEach(function(values, index) {
            datasets.push(
                {
                    data: values,
                    label: categories[index],
                    backgroundColor: categoryColors[index],
                    borderColor: categoryColors[index],
                    order: 2
                }
            )
        });
        // Add 7D moving average
        console.log(data.map(day => day["average_daily_cases_7d"] ?? Number.NaN))
        datasets.push(
            {
                data: data.map(day => day["average_daily_cases_7d"] ?? Number.NaN),
                pointRadius: 0,
                type: 'line',
                fill: false,
                label: '7-day Average',
                borderColor: '#bb0000',
                borderWidth: 2,
                order: 1,
                lineTension: 0
            }
        );
        return datasets;
    } else if(type == 'active') {
        datasets = []
        datasets.push(
            {
                data: data.map(day => day["active_cases"]),
                pointRadius: 0,
                type: 'line',
                fill: false,
                label: 'Active Cases',
                borderColor: '#aaaaaa',
                borderWidth: 1,
                order: 2,
                lineTension: 0
            }
        );
        datasets.push(
            {
                data: data.map(day => day["average_active_cases_7d"] ?? Number.NaN),
                pointRadius: 0,
                type: 'line',
                fill: false,
                label: '7-day Average',
                borderColor: '#bb7700',
                borderWidth: 2,
                order: 1,
                lineTension: 0
            }
        );
        return datasets
    } else if(type == 'pos_rate') {
        datasets = []
        datasets.push(
            {
                data: data.slice(154).map(day => day["positivity_rate"] ?? Number.NaN),
                pointRadius: 0,
                type: 'line',
                fill: false,
                label: '14-day Positivity Rate',
                borderColor: '#0077cc',
                borderWidth: 2,
                order: 1,
                lineTension: 0,
                yAxisID: 'pos_rate'
            }
        );
        datasets.push(
            {
                data: data.slice(154).map(day => day["tests"]["average_14d"] ?? Number.NaN),
                pointRadius: 0,
                type: 'line',
                fill: false,
                label: '14-day Average Daily Tests',
                borderColor: '#aaaaaa',
                borderWidth: 1,
                order: 1,
                lineTension: 0,
                yAxisID: 'tests'
            }
        );
        return datasets
    }
}