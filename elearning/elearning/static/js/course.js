jQuery(function ($) {
    var url = "";
    var closeurl = "";
    $("#saveCourseChanges").click(function (e) {
        $(e.target).attr("data-dismiss", "modal");
        var inputText = $("#formInputModal").val();

        var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
        jQuery.ajax({
            type: 'POST',
            url: url,
            data: {'csrfmiddlewaretoken': token, 'text': inputText},
            dataType: 'json',
            success: function(response) {
                var element;
                if (response["response"]=="ok"){
                    element = $("#okstatus" + response["quiz_id"]);
                }
                else {
                    element = $("#failstatus" + response["quiz_id"]);
                }
                if (element.css('display') == "none"){
                    element.css('display','block');
                }
                var button = $("#button" + response["quiz_id"]);
                button.hide();
            }
        });
    });

    $("#closeQuiz").click(function (e) {
        $(e.target).attr("data-dismiss", "modal");
        var inputText = $("#formInputModal").val();

        var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
        jQuery.ajax({
            type: 'POST',
            url: closeurl,
            data: {'csrfmiddlewaretoken': token, 'text': inputText},
            dataType: 'json',
            success: function(response) {
                var element;
                if (response["response"]=="ok"){
                    element = $("#closeokstatus" + response["quiz_id"]);
                }
                else {
                    element = $("#closefailstatus" + response["quiz_id"]);
                }
                if (element.css('display') == "none"){
                    element.css('display','block');
                }
                var button = $("#closebutton" + response["quiz_id"]);
                button.hide();
            }
        });
    });

    $(".submitBtn").click(function (e) {
        url = $(e.target).val();
    })

    $(".closeBtn").click(function (e) {
        closeurl = $(e.target).val();
    });
});
