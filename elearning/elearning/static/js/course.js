jQuery(function ($) {
    $("#saveCourseChanges").click(function (e) {
        var url = $(e.target).val();
        $.ajax({
            url: url,
            method: "POST",
            data: $("#courseFormPublishModal").serialize()
        });
        $(e.target).attr("data-dismiss", "modal");
    })
});
