$(document).ready(function () {
    $("#btn-predict").click(function () {
        var price = $("#hidden-price").val();
        if(price == ''){
            $("#div-price").html("아직 예측 전입니다.");
        }else{
            $("#div-price").html(price);
        }
    });
});