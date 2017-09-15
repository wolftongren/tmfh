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
    setDabanTable();
    setBeizaTable();
    setYiziTable();
    setZhengchangTable();
    setInterval("setYiziTable()", 30000);
    setInterval("setBeizaTable()", 30000);
    setInterval("setZhengchangTable()", 30000);
    setInterval("setDabanTable()", 5000);

});
