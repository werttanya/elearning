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
        $(nextAnswer).find(":input:text").attr("placeholder", "Answer " + answerNumber).attr("name", question + "answer" + answerNumber).attr("require", "true").val("");
        $(nextAnswer).find(":input:radio").val(question + "answer" + answerNumber);

        $(e.target).before(nextAnswer);
    });

    $("#addQuestionBtn").click(function (e) {
        var parent = $(e.target).parent();
        var tempQuestion = $(originalQuestionAnswer).clone();
        var firstChild = $(tempQuestion).find("#question1");
        var secondChild = tempQuestion.children("#question1Answers");
        var questionNumber = $(parent).children().length - 2;
        var questionsTotal = parseInt($("#numberOfQuestions").val());

        $("#numberOfQuestions").val(questionsTotal + 1);
        tempQuestion.attr("id", "questionAnswer" + questionNumber);
        firstChild.attr("name", "question" + questionNumber);
        firstChild.attr("id", "question" + questionNumber);

        secondChild.attr("id", "question" + questionNumber + "Answers");
        secondChild.children("#question1Answer1").attr("id", "question" + questionNumber + "Answer1").attr("require", "true");
        secondChild.children().find(":input:text").attr("name", "question" + questionNumber + "Answer1");
        secondChild.children().find(":input:radio").attr("name", "question" + questionNumber + "AnswersTrue");

        $(e.target).before(tempQuestion);
    });
});
