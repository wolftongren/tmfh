var chart;
var dataZdp;
var dataFive;
var dataTen;

$(document).ready(function () {

    zdpChart = new Highcharts.Chart({
        chart: {
            renderTo: 'zdpcolchart',
            events: {
                load: st
            }
        },
        title: {
            text: 'zhang, die, ping'
        },
        yAxis: {
            title: {
                text: null
            }
        },
        xAxis: {
            categories: ['zhang', 'die', 'ping'],
            labels: {
                align: 'center'
            }
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            column: {
                colorByPoint: true,
                colors: ['red', 'green', 'grey'],
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        v = 0;
                        for (i in dataZdp) {
                            v += dataZdp[i];
                        }
                        a = this.y / v * 100;
                        return a.toFixed(2) + "%";
                    }
                }
            }
        },
        series: [{
            name: 'overview',
            type: 'column'
        }]

    });


    fiveChart = new Highcharts.Chart({
        chart: {
            renderTo: 'fivecolchart',
            events: {
                load: st
            }
        },
        title: {
            text: '5% view'
        },
        yAxis: {
            title: {
                text: null
            }
        },
        xAxis: {
            categories: ['<-5', '-5-1', '-1-0','0-1','1-5','>5'],
            labels: {
                align: 'center'
            }
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            column: {
                colorByPoint: true,
                colors: ['green','green','green','red','red','red'],
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        v = 0;
                        for (i in dataFive) {
                            v += dataFive[i];
                        }
                        a = this.y / v * 100;
                        return a.toFixed(2) + "%";
                    }
                }
            }
        },
        series: [{
            name: 'overview',
            type: 'column'
        }]

    });

    getZdpData();
    getFiveData();
    getTenData();
});


function getZdpData() {

    $.ajax({
        type: "get",
        url: "/zhangdieping",
        dataType: "json",
        success: function (datax) {
            dataZdp = datax;
            zdpChart.series[0].setData(datax);
        }
    });
}

function getFiveData() {

    $.ajax({
        type: "get",
        url: "/zhangdiefive",
        dataType: "json",
        success: function (datax) {
            dataFive = datax;
            fiveChart.series[0].setData(datax);
        }
    });
}

function getTenData() {

    $.ajax({
        type: "get",
        url: "/zhangdie",
        dataType: "json",
        success: function (datax) {
            data2 = datax;
            zdpChart.series[0].setData(datax);
        }
    });
}

function st() {
    setInterval("getZdpData()", 5000);
    setInterval("getFiveData()", 5000);
    setInterval("getTenData()", 5000);

}