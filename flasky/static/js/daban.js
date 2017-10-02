/**
 * Created by tongren on 17-9-27.
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

$(document).ready(function () {
    setDabanTable();
    setInterval("setDabanTable()", 5000);
});