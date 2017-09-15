/**
 * Created by tongren on 17-9-15.
 */
var chart;
var data2;

$(document).ready(function () {

    piechart = new Highcharts.Chart({
        chart: {
            renderTo: 'piechart',
            type: 'pie',
            events: {
                load: st
            }
        },
        title: {
            text: 'Stock Market Status Monitor - PIE CHART'
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            pie: {
                showlegend: false,
                colors: ['red', 'green', 'grey'],
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        return Highcharts.numberFormat(this.percentage) + '%';
                    }
                }
            }
        },

        series: [{
            name: 'zhangdie distribution'
            //data: data2
            //data: [['zhang', 1],['die', 1], ['ping', 1]]
        }]

    });

    getPieData();
});


function getPieData() {
    $.ajax({
        type: "get",
        url: "/monjson",
        dataType: "json",
        success: function (datax) {
//            data2 = datax;
            piechart.series[0].setData(datax);
        }
    });

}

function st() {
    setInterval("getPieData()", 5000);
}