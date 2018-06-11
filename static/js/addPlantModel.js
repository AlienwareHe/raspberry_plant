function submitPlantModel() {
    var typeId = $('#plantTypeDropMenu2').val()
    if (!typeId){
        alert('请选择植物类型.')
        return
    }
    $('#typeId').val($('#plantTypeDropMenu2').val())
    console.log("植物类型id为",typeId)
    console.log("typeId输入框value为",$('#typeId').val())
    var form = $('#plantModelForm').serialize()
    console.log(form)
    $.ajax({
        url: "/api/plantmodel",
        method: "post",
        data: form,
        success: function (result) {
            if (result) {
                isJump = window.confirm("添加成功，是否查看植物生长类型列表?");
                if (isJump) {
                    location.href = "/plantmodel";
                }
            } else {
                alert("添加失败。。。")
            }

        }
    })
}

$(function () {
    loadPlantType()
});
