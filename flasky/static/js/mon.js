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
            categories: ['zhang', 'die', 'ping'],
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
            name: 'overview',
            data: data2,
            type: 'column'
        }]

    });


    splinechart = new Highcharts.Chart({
        chart: {
            renderTo: 'splinechart',
            type: 'spline',
            events: {
                load: st
            }
        },
        title: {
            text: 'SPLine Chart'
        },
        credits: {
            enabled: false
        },
        yAxis: {
            title: {
                text: 'num'
            }
        },
        xAxis: {
            type: 'linear',
            //categories: ['9:30', '9:31', '9:32','9:33','9:34','9:35','9:36','9:37','9:38','9:39'],
            labels: {
                step: 12
            }
        },
        plogOptions: {
            spline:{
                //pointInterval: 60, //one minute
                //pointStart: Date.UTC(2017,9,16,9,30,0)

            }
        },
        series: [{
            name: 'chuban',
            data: (function(){
                var data=[],i;
                for(i=1;i<=240;i++){
                    data.push({
                        x:i

                    });
                }
                return data;
            })()
        },{
            name: 'yizi',
            data: (function(){
                var data=[],i;
                for(i=1;i<=240;i++){
                    data.push({
                        x:i

                    });
                }
                return data;
            })()
        },{
            name: 'zhangting',
            data: (function(){
                var data=[],i;
                for(i=1;i<=240;i++){
                    data.push({
                        x:i

                    });
                }
                return data;
            })()
        },{
            name: 'beiza',
            data: (function(){
                var data=[],i;
                for(i=1;i<=240;i++){
                    data.push({
                        x:i

                    });
                }
                return data;
            })()
        }]
    });

    getPieData();
    getColumnData();
    getSplineData();
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

function getColumnData() {
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

function getSplineData() {
    $.ajax({
        type: "get",
        url: "/monsplinejson",
        dataType: "json",
        success: function (datax) {
            console.log(datax)
            splinechart.series[0].setData(datax[0]);
            splinechart.series[1].setData(datax[1]);
            splinechart.series[2].setData(datax[2]);
            splinechart.series[3].setData(datax[3]);

        }
    });
}

function st() {
    setInterval("getPieData()", 5000);
    setInterval("getColumnData()", 5000);
    setInterval("getSplineData()", 5000);

}