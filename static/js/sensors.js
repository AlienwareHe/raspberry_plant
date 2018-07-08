window.operationEvents = {
        'click .RoleOfA': function(e, value, row, index) {
            var isActive = ''
            if(row.isActive == 'True'){
                isActive= true
            }else if (row.isActive == 'False'){
                isActive= false
            }
            flag = window.confirm("确定更改"+row.nickname+"传感器有效状态："+isActive+"为"+!isActive+"？");
            if(flag){
                $.get('/api/sensors/'+row.id+'/'+!isActive,function (data) {
                    alert(data)
                    location.reload()
                });
            }
        }
    };

function operationFormatter(value, row, index) {
    if (row.isActive == 'True'){
            return ['<button id="edit_button" type="button" class="RoleOfA btn btn-danger">移出</button>'].join('')
        }else{
            return ['<button id="edit_button" type="button" class="RoleOfA btn btn-success">加入</button>',].join('');
        }
    }

$('#sensorTable').bootstrapTable({
    url:'/api/sensors',
    method: 'get',
    //是否显示行间隔色
    striped: true,
    //是否使用缓存，默认为true，所以一般情况下需要设置一下这个属性（*）
    cache: false,
    columns: [{
        field: 'id',
        title: 'ID',
    }, {
        field: 'name',
        title: '传感器名称'
    }, {
        field: 'class_name',
        title: '类名'
    },{
        field: 'isActive',
        title: '有效状态'
    },{
        filed: 'operate',
        title: '操作',
        formatter: operationFormatter,
        events: operationEvents
    }],
    // 客户端分页
    pagination: true,
    pageNumber: 4,

});


