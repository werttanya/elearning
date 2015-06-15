/**
 * Created by kazakor on 14.06.15.
 */
jQuery(function ($) {
    var counterQuestions = 1;
    var originalQuestionAnswer = $("#questionAnswer1").clone(false);
    $("#newQuizForm").on("click", "#addAnswerBtn", function (e) {
        var parent = $(e.target).parent();

        var firstAnswer = $(parent).children().first();
        var nextAnswer = firstAnswer.clone();
        var question = $(parent).attr("id").slice(0, 9);
        var answerNumber = $(parent).children().length;
        nextAnswer.attr("id", question + "Answer" + answerNumber);
        $(nextAnswer).children(":input").attr("placeholder", "Answer " + answerNumber).attr("name", question + "answer" + answerNumber).attr("require", "true").val("");
        $(e.target).before(nextAnswer);

        console.log("penis");
    });
    $("#addQuestionBtn").click(function (e) {
        var parent = $(e.target).parent();
        var tempQuestion = $(originalQuestionAnswer).clone();
        var firstChild = $(tempQuestion).find("#question1");
        var secondChild = tempQuestion.children("#question1Answers");
        var questionNumber = $(parent).children().length;

        tempQuestion.attr("id", "questionAnswer" + questionNumber);
        firstChild.attr("name", "question" + questionNumber);
        firstChild.attr("id", "question" + questionNumber);

        secondChild.attr("id", "question" + questionNumber + "Answers");
        secondChild.children("#question1Answer1").attr("id", "question" + questionNumber + "Answer1").attr("require", "true");
        secondChild.children().find(":input").attr("name", "question" + questionNumber + "Answer1");
        console.log(secondChild.children(":first").children(":first"));
        $(e.target).before(tempQuestion);
    });
});
