/**
 * Created by tongren on 17-7-26.
 */

function setTable() {
    $('#chubanTable2').bootstrapTable('destroy');

    $('#chubanTable2').bootstrapTable({
        url: '/zhangtingjson',
        columns:[{
            field:'code',
            title:'code'
        }, {
            field:'name',
            title:'name'
        },{
            field:'pchange',
            title:'pchange'
        },{
            field:'a1_b',
            title:'a1_b'
        }
        ]
    });
}

$(document).ready(function () {
    console.log("inside document.ready() function");
    setInterval("setTable()", 5000);

});
