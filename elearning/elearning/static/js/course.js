jQuery(function ($) {
    var id;
    $("#saveCourseChanges").click(function (e) {
        $(e.target).attr("data-dismiss", "modal");
        var inputText = $("#formInputModal").val();
        console.log(url);
        console.log(inputText);

        var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
        jQuery.ajax({
            type: 'POST',
            url: url,
            data: {'csrfmiddlewaretoken': token, 'text': inputText},
            dataType: 'json',
        });
    });

    $("#submitBtn").click(function (e) {
        url = $(e.target).val();
    })
});
