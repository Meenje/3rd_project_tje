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
    $("#note-btn").click(function () {
        var oritext = $("#note").val();
        var text = oritext.replace(/(?:\r\n|\r|\n)/g, '&enter;');
        $.ajax({
            url: "write",
            type: 'POST',
            data: {
                text: text
            },
            success: function (result) {
                alert("저장 성공했습니다.");
            },
            error: function (e) {
                alert("저장 실패!!");
                console.log(e);
            }
        });
    });
});