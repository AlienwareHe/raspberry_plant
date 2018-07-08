function validateRange(value){
    ranges = value.split('~');
    if(ranges.length==2 && !isNaN(ranges[0]) && !isNaN(ranges[1])){
        return true;
    }else{
        return false;
    }
}
// 删除选中行
function delSelected(){
    var rows = $('#plantModelTable').bootstrapTable('getSelections');
    var delIds = new Array();
    console.log(rows)
    for (var i = 0;i<rows.length;i++){
        delIds.push(rows[i].id)
    }
    $.ajax({
        url: '/api/plantmodel',
        method: 'DELETE',
        // 参数为数组时需要先转化成json字符串
        data: {'delIds':JSON.stringify(delIds)},
        success: function (result) {
            alert(result);
            $('#plantModelTable').bootstrapTable('refresh',{slient:true});
        },
        error: function (result) {
            alert(result);
            $('#plantModelTable').bootstrapTable('refresh',{slient:true});
        }
    });
}

$('#plantModelTable').bootstrapTable({
    url: '/api/plantmodel',
    clickToSelect: true,
    showRefresh: true,
    cache: false,
    toolbar: '#toolbar',
    columns: [{
        checkbox: true,
    },{
        field: 'id',
        title: 'ID'
    },{
        field: 'type',
        title: '植物类型'
    },{
        field: 'growStatus',
        title: '生长阶段'
    },{
        field: 'airtemp',
        title: '空气温度范围',
        editable: {
            type: 'text',
            title: '植物类型',
            validate: function (v) {
                if(!validateRange){
                    return '植物类型不能为空';
                }
            }
        }
    },{
        field: 'airhum',
        title: '空气湿度范围',
        editable: {
            type: 'text',
            title: '空气湿度范围',
            validate: function (v) {
                if(!validateRange){
                    return '空气湿度范围不能为空';
                }
            }
        }
    },{
        field: 'light',
        title: '光照强度范围',
        editable: {
            type: 'text',
            title: '光照强度范围',
            validate: function (v) {
                if(!validateRange){
                    return '光照强度范围不能为空';
                }
            }
        }
    },{
        field: 'soilhumi',
        title: '土壤湿度范围',
        editable: {
            type: 'text',
            title: '土壤湿度范围',
            validate: function (v) {
                if(!validateRange){
                    return '土壤湿度范围不能为空';
                }
            }
        }
    }],
    pagination: true,
    // checkbox名字。否则编辑时会被当作row中一个属性即{0:true/false}
    selectItemName: 'checkbox',
    onEditableSave: function (field, row, oldValue, $el) {
        var jsonData = JSON.stringify(row);
        $.ajax({
            type: 'post',
            url: '/api/editPlantmodel',
            data: jsonData,
            // 这才是请求头设置
            contentType: 'application/json;charset=UTF-8',
            success: function (result) {
                alert(result)
            },
            error: function (result) {
                alert("编辑失败")
            }
        })
    }
});