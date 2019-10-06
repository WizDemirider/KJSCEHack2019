
        var options = {
            chart: {
                height: 350,
                type: 'bar',
            },
			colors:['#6610f2'],
            plotOptions: {
                bar: {
                    dataLabels: {
                        position: 'top', // top, center, bottom
                    },
                }
            },
            dataLabels: {
                enabled: true,
                formatter: function (val) {
                    return val + "%";
                },
                offsetY: -20,
                style: {
                    fontSize: '12px',
                    colors: ["#304758"]
                }
            },
            series: [{
                name: 'Percentile',
                data: [76, 58, 60, 52, 78, 80, 64, 46, 70, 55]
            }],
            xaxis: {
                categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"],
                position: 'top',
                labels: {
                    offsetY: -18,

                },
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false
                },
                crosshairs: {
                    fill: {
                        type: 'gradient',
                        gradient: {
                            colorFrom: '#FD7E14',
                            colorTo: ' #6610f2;',
                            stops: [0, 100],
                            opacityFrom: 0.7,
                            opacityTo: 1,
                        }
                    }
                },
                tooltip: {
                    enabled: true,
                    offsetY: -35,

                }
            },
            fill: {
                gradient: {
                    shade: 'light',
                    type: "horizontal",
                    shadeIntensity: 0.25,
                    gradientToColors: undefined,
                    inverseColors: true,
                    opacityFrom: 1,
                    opacityTo: 1,
                    stops: [50, 0, 100, 100]
                },
            },
            yaxis: {
                axisBorder: {
                    show: false
                },
                axisTicks: {
                    show: false,
                },
				max: 100,
                labels: {
                    show: false,
                    formatter: function (val) {
                        return val + "%";
                    }
                }

            },
            title: {
                text: 'Percentile over the past few months',
                floating: true,
                offsetY: 320,
                align: 'center',
                style: {
                    color: '#444'
                }
            },
        }


        var options1 = {
            chart: {
                height: 350,
                type: 'radialBar',
            },
			colors:['#FD7E14'],
            plotOptions: {
                radialBar: {
                    hollow: {
                        size: '70%',
                    }
                },
            },
            series: [30],
            labels: ['TOTAL SCORE'],

        }
        var chart = new ApexCharts(
            document.querySelector("#chart"),
            options
        );

        chart.render();
		        
				
		var chart1 = new ApexCharts(
            document.querySelector("#chart1"),
            options1
        );
		chart1.render();
