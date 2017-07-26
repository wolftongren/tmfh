var chart;
var data2;

$(document).ready(function () {

    chart = new Highcharts.Chart({
        chart: {
            renderTo: 'columnchart',
            events: {
                load: st
            }
        },
        title: {
            text: 'Stock Market Status Monitor'
        },
        xAxis: {
            categories: ['shangzhang', 'xiadie', 'pingpan'],
            labels: {
                align: 'center'
            }
        },
        yAxis: {
            title: {
                text: 'No. of stocks'
            }
        },

        plotOptions: {
            column: {
                colorByPoint: true,
                colors: ['red', 'green', 'grey'],
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        v = 0;
                        for (i in data2) {
                            v += data2[i];
                        }
                        a = this.y / v * 100;
                        return a.toFixed(2) + "%";
                    }
                }
            }
        },

        series: [{
            name: 'zhangdie distribution',
            data: data2,
            type: 'column'
        }]

    });

});


function getData() {

    $.ajax({
        type: "get",
        url: "/zhangdie",
        dataType: "json",
        success: function (datax) {
            data2 = datax;
            chart.series[0].setData(datax);
        }
    });
}

function st() {
    setInterval("getData()", 5000);
}