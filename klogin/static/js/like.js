function hover_full(element) {
    element.setAttribute('src', '../../static/img_main/full_heart.png');
}

function hover_empty(element) {
    element.setAttribute('src', '../../static/img_main/empty_heart.jpg');
}

// csrf 토큰 보내줄때 쓰는 함수
function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function () {
    var token = $("#csrf-input").val();
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", token);
            }
        }
    });
    $("#like-icon").click(function () {
        var present = String($(this).attr('src').trim());
        var check = "";
        if (present == '../../static/img_main/full_heart.png') {
            $(this).attr('src', '../../static/img_main/full_heart.png');
            $(this).attr('onmouseover', "hover_empty(this);");
            $(this).attr('onmouseout', "hover_full(this);");
            check = "insert";
        } else {
            $(this).attr('src', '../../static/img_main/empty_heart.jpg');
            $(this).attr('onmouseover', "hover_full(this);");
            $(this).attr('onmouseout', "hover_empty(this);");
            check = "delete";
        }
        var code = $("#small-code").text();

        $.ajax({
            url: "like",
            type: 'POST',
            data: {
                check: check,
                stock_code : code
            },
            success: function (result) {
                console.log(result);
            },
            error: function (e) {
                alert("실패");
                console.log(e);
            }
        });
    });
});