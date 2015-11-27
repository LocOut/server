function createChart(id, options, name){
    var newChart;
    $(function () {

        $("#device" + id).highcharts({

            chart: {
                type: 'gauge',
                backgroundColor: null,
                plotBackgroundColor: null,
                plotBackgroundImage: null,
                plotBorderWidth: 0,
                plotShadow: false
            },

            title: {
                text: name,
                style: {'color':'#FFFFFF'}
            },

            pane: {
                startAngle: -150,
                endAngle: 150,
                background: [{
                    backgroundColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0, '#FFF'],
                            [1, '#333']
                        ]
                    },
                    borderWidth: 0,
                    outerRadius: '109%'
                }, {
                    backgroundColor: {
                        linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                        stops: [
                            [0, '#333'],
                            [1, '#FFF']
                        ]
                    },
                    borderWidth: 1,
                    outerRadius: '107%'
                }, {
                    // default background
                }, {
                    backgroundColor: '#DDD',
                    borderWidth: 0,
                    outerRadius: '105%',
                    innerRadius: '103%'
                }]
            },

            // the value axis
            yAxis: {
                min: 0,
                max: 100,

                minorTickInterval: 'auto',
                minorTickWidth: 1,
                minorTickLength: 10,
                minorTickPosition: 'inside',
                minorTickColor: '#666',

                tickPixelInterval: 30,
                tickWidth: 2,
                tickPosition: 'inside',
                tickLength: 10,
                tickColor: '#666',
                labels: {
                    step: 2,
                    rotation: 'auto'
                },
                title: {
                    text: '%'
                },
                plotBands: [{
                    from: 0,
                    to: 50,
                    color: '#DF5353' // red
                }, {
                    from: 50,
                    to: 75,
                    color: '#DDDF0D' // yellow
                }, {
                    from: 75,
                    to: 100,
                    color: '#55BF3B' // green
                }]
            },

            series: [{
                name: 'Trust Level',
                data: options,
                tooltip: {
                    valueSuffix: ' %'
                }
            }]

        },
        function (chart) {
            newChart = chart;

        });
    });
    return newChart;
}