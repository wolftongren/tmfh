/**
 * Created by tongren on 17-7-26.
 */

function setYiziTable() {
//    $('#yiziTable').bootstrapTable('destroy');
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
        }
        ]
    });
}

function setBeizaTable() {
//    $('#beizaTable').bootstrapTable('destroy');
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

 //   $('#zhengchangTable').bootstrapTable('destroy');
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
    console.log("inside document.ready() function");
    setInterval("setYiziTable()", 5000);
    setInterval("setBeizaTable()", 5000);
    setInterval("setZhengchangTable()", 5000);

});
