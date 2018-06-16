var togglecounter1 = false,
    togglecounter2 = false,
    togglecounter3 = false,
    togglecounter4 = false,
    togglecounter5 = false;
var togglecounterlist = {
    togglecounter1,
    togglecounter2,
    togglecounter3,
    togglecounter4,
    togglecounter5
}
var chartname = document
    .getElementById("myChart")
    .className;
console.log(chartname)
var ctx = document
    .getElementById("myChart")
    .getContext("2d");
var gradientFill = ctx.createLinearGradient(0, 400, 0, 50);
gradientFill.addColorStop(0, "rgba(128, 182, 244, 0.3)");
gradientFill.addColorStop(1, "rgba(244, 144, 128, 0.3)");

if (chartname != 'chart1') {
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [
                "Mo 24/7", "Di 25/7", "Wo 26/7", "Do 27/7", "Vr 28/7"
            ],
            datasets: [
                {
                    label: 'Temperatuur',

                    data: [
                        21.4, 17.5, 18.6, 10.1, 15

                    ],
                    backgroundColor: 'rgba(244, 144, 128, 0.3)',
                    borderColor: ['rgba(244, 144, 128, 1)'],
                    borderWidth: 1,
                    yAxisID: 'A'

                }, {
                    label: 'Luchtvochtigheid',
                    data: [
                        45, 56, 70, 50, 35

                    ],
                    backgroundColor: "rgba(128, 182, 244, 0.45)",
                    borderColor: ['rgba(128, 182, 244, 1)'],
                    borderWidth: 1,
                    yAxisID: 'B'
                }, {
                    label: 'Windsnelheid',
                    data: [
                        11, 1, 3, 14, 15

                    ],
                    backgroundColor: 'rgba(146, 128, 244, 0.5)',
                    borderColor: ['rgba(146, 128, 244, 1)'],
                    borderWidth: 1,
                    yAxisID: 'A'
                }, {
                    label: 'UV Index',
                    data: [
                        4, 6, 3, 5, 6

                    ],
                    backgroundColor: 'rgb(244, 232, 128,0.5)',
                    borderColor: ['rgb(244, 232, 128,1)'],
                    borderWidth: 1,
                    yAxisID: 'A'
                }
            ]
        },
        options: {
            legend: {
                display: true
            },
            tooltips: {
                mode: 'x',
                position: 'nearest',
                titleFontSize: 16,
                backgroundColor: 'rgba(255, 255, 255, 0.8)',

                titleFontColor: '#111',
                bodyFontColor: '#111',
                bodyFontSize: 14,
                displayColors: false,
                xPadding: 8,
                yPadding: 8,

                caretSize: 0
            },
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        id: 'A',
                        type: 'linear',
                        position: 'left',
                        ticks: {
                            beginAtZero: true
                        }
                    }, {
                        id: 'B',
                        type: 'linear',
                        position: 'right',
                        ticks: {
                            max: 0,
                            min: 100,
                            beginAtZero: true

                        },
                        stepSize: 10
                    }
                ]
            }
        }
    });
} else {
    var myChart2 = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [
                "Mo 24/7", "Di 25/7", "Wo 26/7", "Do 27/7", "Vr 28/7"
            ],
            datasets: [
                {
                    label: 'Temperatuur',

                    data: [
                        21.4, 17.5, 18.6, 10.1, 15

                    ],
                    backgroundColor: 'rgba(244, 144, 128, 0.3)',
                    borderColor: ['rgba(244, 144, 128, 1)'],
                    borderWidth: 1,
                    yAxisID: 'A'

                }, {
                    label: 'Neerslag',
                    data: [
                        45, 56, 70, 50, 35

                    ],
                    backgroundColor: "rgba(128, 182, 244, 0.45)",
                    borderColor: ['rgba(128, 182, 244, 1)'],
                    borderWidth: 1,
                    yAxisID: 'B'
                }, {
                    label: 'Windsnelheid',
                    data: [
                        11, 1, 3, 14, 15

                    ],
                    backgroundColor: 'rgba(146, 128, 244, 0.5)',
                    borderColor: ['rgba(146, 128, 244, 1)'],
                    borderWidth: 1,
                    yAxisID: 'A'
                }
            ]
        },
        options: {
            legend: {
                display: true
            },
            tooltips: {
                mode: 'x',
                position: 'nearest',
                titleFontSize: 16,
                backgroundColor: 'rgba(255, 255, 255, 0.8)',

                titleFontColor: '#111',
                bodyFontColor: '#111',
                bodyFontSize: 14,
                displayColors: false,
                xPadding: 8,
                yPadding: 8,

                caretSize: 0
            },
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [
                    {
                        id: 'A',
                        type: 'linear',
                        position: 'left',
                        ticks: {
                            beginAtZero: true
                        }
                    }, {
                        id: 'B',
                        type: 'linear',
                        position: 'right',
                        ticks: {
                            max: 0,
                            min: 100,
                            beginAtZero: true

                        },
                        stepSize: 10
                    }
                ]
            }
        }
    });
}
function toggleChart(i, chartnr) {
    console.log(i)

    if (chartnr == 0) {
        var toggle = 'togglecounter' + (i + 1);
        console.log(togglecounterlist[toggle])
        togglecounterlist[toggle] = !togglecounterlist[toggle]
        myChart
            .getDatasetMeta(i)
            .hidden = togglecounterlist[toggle];
        myChart.update();
    } else {
        var toggle = 'togglecounter' + (i + 1);
        console.log(togglecounterlist[toggle])
        togglecounterlist[toggle] = !togglecounterlist[toggle]
        myChart2
            .getDatasetMeta(i)
            .hidden = togglecounterlist[toggle];
        myChart2.update();
    }
}
