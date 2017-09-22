var dataZdp;


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
            categories: ['die', 'zhang', 'ping'],
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
                colors: ['green', 'red', 'grey'],
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
//            categories: ['<-9', '-9', '-8','-7','-6','-5','-4','-3','-2','-1','1','2','3','4','5','6','7','8','9','>9'],
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

    getZdfData();

});



function getZdfData() {

    $.ajax({
        type: "get",
        url: "/zhangdiefu",
        dataType: "json",
        success: function (datax) {
            dataZdp = [0,0,0];
            dataZdp[0] = datax[9];
            dataZdp[1] = datax[11];
            dataZdp[2] = datax[10];
            zdpChart.series[0].setData(dataZdp);

            var dataFive = [];
            dataFive[0] = datax[1]; // <-8
            dataFive[1] = datax[6]-datax[1]; // -8 ~ -3
            dataFive[2] = datax[9]-datax[6]; // -3 ~ 0
            dataFive[3] = datax[11]-datax[14]; // 0 ~ 3
            dataFive[4] = datax[14]-datax[19]; // 3 ~ 8
            dataFive[5] = datax[19]; // >8
            fiveChart.series[0].setData(dataFive);

            var dataTen = [];
            dataTen[0] = datax[0]; //<-9
            dataTen[1] = datax[1]-datax[0];//-9 ~ -8
            dataTen[2] = datax[2]-datax[1];
            dataTen[3] = datax[3]-datax[2];
            dataTen[4] = datax[4]-datax[3];
            dataTen[5] = datax[5]-datax[4];
            dataTen[6] = datax[6]-datax[5];
            dataTen[7] = datax[7]-datax[6];
            dataTen[8] = datax[8]-datax[7];
            dataTen[9] = datax[9]-datax[8];
            dataTen[10] = datax[11]-datax[12];
            dataTen[11] = datax[12]-datax[13];
            dataTen[12] = datax[13]-datax[14];
            dataTen[13] = datax[14]-datax[15];
            dataTen[14] = datax[15]-datax[16];
            dataTen[15] = datax[16]-datax[17];
            dataTen[16] = datax[17]-datax[18];
            dataTen[17] = datax[18]-datax[19];
            dataTen[18] = datax[19]-datax[20];
            dataTen[19] = datax[20];
            tenChart.series[0].setData(dataTen);
        }
    });
}

function st() {
     setInterval("getZdfData()", 5000);

}