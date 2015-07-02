jQuery(function ($) {
    var url = "";
    $("#saveCourseChanges").click(function (e) {
        $(e.target).attr("data-dismiss", "modal");
        var inputText = $("#formInputModal").val();

        var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
        jQuery.ajax({
            type: 'POST',
            url: url,
            data: {'csrfmiddlewaretoken': token, 'text': inputText},
            dataType: 'json',
            contentType: "application/json; charset=utf-8",
            success: function(response) {
                if (response["response"]=="ok"){
                    status = $("#okstatus"+response["quiz_id"]);
                }
                else {
                    status = $("#failstatus"+response["quiz_id"]);
                }
                if (status.css('display') == "none"){
                    status.css('display','block');
                }
            }
        });
    });

    $(".submitBtn").click(function (e) {
        url = $(e.target).val();
    });
});
