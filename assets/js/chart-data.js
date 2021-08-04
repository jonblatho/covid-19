function chartLabels(type, data) {
    var dates = data.map(day => day["date"]);

    return dates
}

function fillDataset(values, label, color) {
    return {
        data: values,
        pointRadius: 0,
        type: 'line',
        fill: 'origin',
        label: label,
        backgroundColor: color,
        borderWidth: 2,
        order: 1,
        lineTension: 0
    };
}

function primaryLineDataset(values, label, color) {
    return {
        data: values,
        pointRadius: 0,
        type: 'line',
        fill: false,
        label: label,
        borderColor: color,
        borderWidth: 2,
        order: 1,
        lineTension: 0
    };
}

function secondaryLineDataset(values, label, color='#aaaaaa', width=1) {
    return {
        data: values,
        pointRadius: 0,
        type: 'line',
        fill: false,
        label: label,
        borderColor: color,
        borderWidth: width,
        order: 1,
        lineTension: 0
    };
}

function chartData(type, data) {
    datasets = [];
    if(type == 'total' || type == 'new') {
        if(type == 'total') {
            var data_key = "total_cases";
        } else if(type == 'new') {
            var data_key = "new_cases";
        }
        keys.forEach(function(category_key, index) {
            var dict = {
                data: data.map(day => day[data_key][category_key]),
                label: categories[index],
                backgroundColor: categoryColors[index],
            };
            if(type == 'total') {
                dict.fill = 'origin';
                dict.pointRadius = 0;
            } else if(type == 'new') {
                dict.borderColor = categoryColors[index];
                dict.order = 2;
                dict.categoryPercentage = 1.0;
                dict.barPercentage = 1.0;
            }
            datasets.push(dict);
        })
        if(type == 'new') {
            // Add 7D moving average
            datasets.push({
                data: data.map(day => day["average_daily_cases_7d"] ?? Number.NaN),
                pointRadius: 0,
                type: 'line',
                fill: false,
                label: '7-day Average',
                borderColor: '#bb0000',
                borderWidth: 2,
                order: 1,
                lineTension: 0
            });
        }
    } else if (type == 'risk_level') {
        datasets.push(primaryLineDataset(data.map(day => day["average_daily_cases_14d_100k"] ?? Number.NaN), '14-day Average Daily Cases per 100K', '#000'));
    } else if (type == 'active') {
        datasets.push(primaryLineDataset(data.map(day => day["average_active_cases_7d"] ?? Number.NaN), '7-day Average', '#bb7700'));
        datasets.push(secondaryLineDataset(data.map(day => day["active_cases"]), 'Active Cases'));
        datasets.push(secondaryLineDataset(data.map(day => day["hospitalizations"]), 'Hospitalizations', color='#0bc6c0', width=2));
    } else if(type == 'pos_rate') {
        datasets.push(primaryLineDataset(data.map(day => day["positivity_rate"] ?? Number.NaN), '14-day Positivity Rate', '#0077cc'));
        var averageDataset = secondaryLineDataset(data.map(day => day["tests"]["average_14d"] ?? Number.NaN), '14-day Average Daily Tests');
        averageDataset.yAxisID = 'y_tests';
        datasets.push(averageDataset);
    } else if(type == 'vaccine_doses') {
        datasets.push(primaryLineDataset(data.map(day => day["doses_average_7d"] ?? Number.NaN), '7-day Average', '#8915b0'));
        var averageDataset = secondaryLineDataset(data.map(day => day["doses"] ?? Number.NaN), 'Doses Administered');
        datasets.push(averageDataset);
    } else if(type == 'vaccine_residents') {
        datasets.push(fillDataset(data.map(day => day["completed"] ?? Number.NaN), 'Fully Vaccinated', '#13d694'));
        var averageDataset = fillDataset(data.map(day => day["initiated"] ?? Number.NaN), 'Initiated Vaccination', '#0fa673');
        datasets.push(averageDataset);
    }
    return datasets;
}