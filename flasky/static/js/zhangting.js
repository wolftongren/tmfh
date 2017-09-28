/**
 * Created by tongren on 17-7-26.
 */

function setDabanTable() {
    $('#dabanTable').bootstrapTable('destroy');
    $('#dabanTable').bootstrapTable({
        url: '/dabantishijson',
        columns: [{
            field: 'id',
            title: 'id'
        }, {
            field: 'code',
            title: 'code'
        }, {
            field: 'name',
            title: 'name'
        }, {
            field: 'zf',
            title: 'zf'
        }, {
            field: 'high',
            title: 'high'
        }, {
            field: 'chubanCount3',
            title: 'cb3'
        }, {
            field: 'beizaLv3',
            title: 'beiza%3'
        }, {
            field: 'gaokaiLv3',
            title: 'gaokai%3'
        }, {
            field: 'baobenLv3',
            title: 'baoben%3'
        }, {
            field: 'shoupanLv3',
            title: 'shoupan%3'
        }, {
            field: 'chubanCount',
            title: 'cb'
        }, {
            field: 'beizaLv',
            title: 'beiza%'
        }, {
            field: 'gaokaiLv',
            title: 'gaokai%'
        }, {
            field: 'baobenLv',
            title: 'baoben%'
        }, {
            field: 'shoupanLv',
            title: 'shoupan%'
        }
        ]
    });
}


function setYiziTable() {
    $('#yiziTable').bootstrapTable('destroy');
    $('#yiziTable').bootstrapTable({
        url: '/yizijson',
        columns: [{
            field: 'id',
            title: 'id'
        }, {
            field: 'code',
            title: 'code'
        }, {
            field: 'name',
            title: 'name'
        }, {
            field: 'timeToMarket',
            title: 'timeToMarket'
        }
        ]
    });
}

function setBeizaTable() {
    $('#beizaTable').bootstrapTable('destroy');
    $('#beizaTable').bootstrapTable({
        url: '/beizajson',
        columns: [{
            field: 'id',
            title: 'id'
        }, {
            field: 'code',
            title: 'code'
        }, {
            field: 'name',
            title: 'name'
        }, {
            field: 'industry',
            title: 'industry'
        }, {
            field: 'cbTime',
            title: 'cbTime'
        }, {
            field: 'zf',
            title: 'zf'
        }
        ]
    });
}


function setZhengchangTable() {
    console.log("inside setZhengchangTable()...")
    $('#zhengchangTable').bootstrapTable('destroy');
    $('#zhengchangTable').bootstrapTable({
        url: '/zhengchangjson',
        columns: [{
            field: 'id',
            title: 'id'
        }, {
            field: 'code',
            title: 'code'
        }, {
            field: 'name',
            title: 'name'
        }, {
            field: 'industry',
            title: 'industry'
        }, {
            field: 'cbTime',
            title: 'cbTime'
        }, {
            field: 'isBeiza',
            title: 'isBeiza'
        }
        ]
    });


}

$(document).ready(function () {

    splinechart = new Highcharts.Chart({
        chart: {
            renderTo: 'splinechartzhangting',
            type: 'spline',
            events: {
                load: st
            }
        },
        title: {
            text: 'Zhangting Related Trends'
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
        plotOptions: {
            spline: {
                linewidth: 4,
                states: {
                    hover: {
                        linewidth: 5
                    }
                },
                marker: {
                    enabled: false
                }
            }
        },
        series: [
            {
                name: 'yizi',
                color: 'blue'
            }, {
                name: 'zhangting',
                color: 'red'
            }, {
                name: 'beiza',
                color: 'green'
            }]
    });


    //setDabanTable();
    //setInterval("setDabanTable()", 5000);

    getSplineData();

    setBeizaTable();
    setYiziTable();
    setZhengchangTable();
    setInterval("setYiziTable()", 10000);
    setInterval("setBeizaTable()", 10000);
    setInterval("setZhengchangTable()", 10000);

});

function getSplineData() {
    $.ajax({
        type: "get",
        url: "/zhangtingsplinejson",
        dataType: "json",
        success: function (datax) {
            console.log(datax)
            splinechart.series[0].setData(datax[0]);
            splinechart.series[1].setData(datax[1]);
            splinechart.series[2].setData(datax[2]);

        }
    });
}

function st() {
    setInterval("getSplineData()", 50000);
}
