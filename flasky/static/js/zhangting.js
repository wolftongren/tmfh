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
            field: 'chubanCount3',
            title: 'chubanCount3'
        }, {
            field: 'beizaLv3',
            title: 'beizaLv3'
        }, {
            field: 'gaokaiLv3',
            title: 'gaokaiLv3'
        }, {
            field: 'baobenLv3',
            title: 'baobenLv3'
        }, {
            field: 'shoupanLv3',
            title: 'shoupanLv3'
        }, {
            field: 'chubanCount',
            title: 'chubanCount'
        }, {
            field: 'beizaLv',
            title: 'beizaLv'
        }, {
            field: 'gaokaiLv',
            title: 'gaokaiLv'
        }, {
            field: 'baobenLv',
            title: 'baobenLv'
        }, {
            field: 'shoupanLv',
            title: 'shoupanLv'
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
        }
        ]
    });


}

$(document).ready(function () {
    setDabanTable();
    setBeizaTable();
    setYiziTable();
    setZhengchangTable();
    setInterval("setYiziTable()", 5000);
    setInterval("setBeizaTable()", 5000);
    setInterval("setZhengchangTable()", 5000);
    setInterval("setDabanTable()", 5000);

});
