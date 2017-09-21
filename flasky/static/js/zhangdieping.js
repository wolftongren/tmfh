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
            text: 'main view'
        },
        yAxis: {
            title: {
                text: null
            }
        },
        xAxis: {
            categories: ['die', 'ping', 'zhang'],
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
                colors: ['green', 'grey', 'red'],
                dataLabels: {
                    enabled: true,
                    formatter: function () {
                        v = 0;
                        for (i in dataZdp) {
                            v += dataZdp[i].y;
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
            categories: ['<-8', '-8-3', '-3-0','0-3','3-8','>8'],
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
                    enabled: true

                }
            }
        },
        series: [{
            name: 'overview',
            type: 'column'
        }]

    });

    tenChart = new Highcharts.Chart({
        chart: {
            renderTo: 'tencolchart',
            events: {
                load: st
            }
        },
        title: {
            text: '1% view'
        },
        yAxis: {
            title: {
                text: null
            }
        },
        xAxis: {
            categories: ['<-9', '-9-8', '-8-7','-7-6','-6-5','-5-4','-4-3','-3-2','-2-1','-1-0','0-1','1-2','2-3','3-4','4-5','5-6','6-7','7-8','8-9','>9'],
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
                colors: ['green','green','green','green','green','green','green','green','green','green','red','red','red','red','red','red','red','red','red','red'],
                dataLabels: {
                    enabled: true

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


function getTenData() {

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

function getZdpData() {

    $.ajax({
        type: "get",
        url: "/zhangdieten",
        dataType: "json",
        success: function (datax) {
            dataZdp[0] = datax[11];
            dataZdp[1] = datax[9];
            dataZdp[2] = datax[10];
            tenChart.series[0].setData(dataZdp);

            dataFive[0] = 
        }
    });
}

function getZdfData() {

    $.ajax({
        type: "get",
        url: "/zhangdiefu",
        dataType: "json",
        success: function (datax) {
            dataZdp[0] = datax[9];
            dataZdp[1] = datax[10];
            dataZdp[2] = datax[11];
            zdpChart.series[0].setData(dataZdp);
        }
    });
}

function st() {
     setInterval("getZdfData()", 5000);
//    setInterval("getZdpData()", 5000);
//    setInterval("getFiveData()", 5000);
//    setInterval("getTenData()", 5000);

}