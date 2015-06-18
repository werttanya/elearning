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
        });
    });

    $(".submitBtn").click(function (e) {
        url = $(e.target).val();
    });
});
