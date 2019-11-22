$(document).ready(function () {
    var price_now = $("#blind_price").val();
    var date_now = $("#blind_date").val();
    var name = $("#strong-name").text();

    const array = Array.from(Array(502), () => Array());
    var dt;
    var y, m, d;
    y = Number(date_now.substring(0,4));
    m = Number(date_now.substring(4,6)) - 1;
    d = Number(date_now.substring(6,8));

    array[0].push("date");
    array[0].push(name);

    array[501].push(new Date(y, m, d));
    array[501].push(price_now);

    var index = 500;
    var dt;
    var y, m, d;
    $(".date").each(function() {
        dt = $(this).val();
        y = Number(dt.substring(0,4));
        m = Number(dt.substring(4,6)) - 1;
        d = Number(dt.substring(6,8));
        array[index].push(new Date(y, m, d));
        index --;
    });
    index = 500;
    $(".close").each(function() {
        array[index].push(Number($(this).val()));
        index --;
    });

    google.charts.load('current', {'packages':['corechart']});
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
        var data = google.visualization.arrayToDataTable(array);
        var chart = new google.visualization.LineChart(document.getElementById('graph_div'));
        var options = {
            chartArea: {'width': '95%', 'height': '85%'},
            legend: 'none'
        };
        chart.draw(data, options);
    }

});