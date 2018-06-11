
$('input[name="my-checkbox"]').bootstrapSwitch({
        "onColor" : "success",
        "offColor" : "danger",
        "onText" : "启动",
        "offText" : "停止",
        onInit: function(event,state){
          $.get("/api/runstate",function (result) {
                if (result == 'True'){
                    $('input[name="my-checkbox"]').bootstrapSwitch('state',true,true)
                }else if (result == 'False'){
                    $('input[name="my-checkbox"]').bootstrapSwitch('state',false,true)
                }
          });
        },
        onSwitchChange : function (event,state) {
            console.log('切换开关状态为'+state)
            if(state){
                // 启动
                // 先设置植物类型
                $('#runModal').modal({show:true})
                loadPlantType();
            }else{
                // 停止
                $.get("/api/run?mode=off")
            }
        }
    });

function loadPlantType() {
    $.get('/api/planttypes?isAll=True', function (data) {
        build_dropdown( data, $( '#plantTypeDropMenu1' ), '请选择...' );
    })
    $.get('/api/planttypes?isAll=False',function(data){
        build_dropdown( data, $( '#plantTypeDropMenu2' ), '请选择...' );
    })
}

function build_dropdown( data, element, defaultText ){
	element.empty().append( '<option value="">' + defaultText + '</option>' );
	if( data ){
		$.each( data, function( index,ele ){
			element.append( '<option value="' + ele.id + '">' + ele.type + '</option>' );
		} );
	}
}

function submitPlantType(){
    var selectPlantTypeId = $('#plantTypeDropMenu1').val()
    if (!isNaN(selectPlantTypeId) && selectPlantTypeId>=1){
        $.get("/api/run?mode=on&plantTypeId="+selectPlantTypeId,function (result) {
            alert(result)
            $('#runModal').modal('hide')
        })
    }else{
        alert('请勾选植物类型');
        loadPlantType();
    }
}

function closeRunMOdal(){
    // 将开关状态设为相反
    $('input[name="my-checkbox"]').bootstrapSwitch('toggleState',true)
}


function toggleEditModal(key){
    $('#editKey').val(key);
    $('#editModal').modal('show');
}



function editRasperryConfig(){
    var key = $('#editKey').val();
    var value = $('#editInputValue').val();
    $.ajax({
        url: "/api/config/"+key+"/"+value,
        method: "PUT",
        success: function (data) {
            alert(data)
            $('#editModal').modal({show:false});
            // 刷新页面
            location.reload()
        }
    });

}