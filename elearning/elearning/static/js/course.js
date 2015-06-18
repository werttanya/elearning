jQuery(function ($) {
    $("#saveCourseChanges").click(function (e) {
        var url = $(e.target).val();
         $(e.target).attr("data-dismiss", "modal");
         $("#courseFormPublishModal").submit();
    })
});
