$(document).ready(function() {
    window.AudioContext = window.AudioContext || window.webkitAudioContext;
    navigator.getUserMedia = ( navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia || navigator.msGetUserMedia);
    window.URL = window.URL || window.webkitURL;

    var audio_context = new AudioContext;

    if (!('webkitSpeechRecognition' in window)) {
        upgrade();
    }

    $("#add-word").click(function(e) {
        e.preventDefault();
        if (!$("#new-word").val()) {
            return;
        }
        $("#btn-toggle").prop("disabled", false);
        $("#word-list").append($("<div class='word-item'><span class='word-item-text'>" + $("<div />").text($("#new-word").val()).html() + "</span><span class='word-item-delete'>&times;</span></div>"));
        $("#new-word").val("");
    });
    $("#new-word").keyup(function(e) {
        if (e.keyCode == 13) {
            $("#add-word").click();
        }
    });
    $("#word-list").on("click", ".word-item-delete", function(e) {
        e.preventDefault();
        $(this).parent().remove();
        if ($("#word-list .word-item").length == 0) {
            $("#btn-toggle").prop("disabled", true);
        }
    });
    $("#btn-toggle").click(function(e) {
        e.preventDefault();
        if ($("#word-list .word-item").length == 0) {
            return;
        }
        load_random_practice_word();
    });
});
function load_random_practice_word() {
    load_practice_word($("#word-list .word-item").eq(Math.floor(Math.random() * $("#word-list .word-item").length)).find(".word-item-text").text());
}
var recognition = new webkitSpeechRecognition();
function quiz_word() {
    var final_transcript = '';
    recognition.lang = 'zh-CN';
    recognition.onresult = function(event) {
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                if (event.results[i][0].transcript) {
                    final_transcript += event.results[i][0].transcript;
                }
            }
        }
    }
    recognition.onend = function(event) {
        console.log(final_transcript);
        check_answer(final_transcript);
    }
    recognition.start();
}
function check_answer(usrans) {
    if (usrans == $("#practice-word").text()) {
        $("#practice-word").css("background-color", "green");
    }
    else {
        $("#practice-word").css("background-color", "red");
    }
    setTimeout(function() {
        $("#practice-word").css("background-color", "");
        load_random_practice_word();
    }, 3000);
}
function load_practice_word(word) {
    $("#practice-word").text(word);
    quiz_word();
}
