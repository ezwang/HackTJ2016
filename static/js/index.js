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
            playing = false;
        }
    });
    var playing = false;
    $("#btn-toggle").click(function(e) {
        e.preventDefault();
        if ($("#word-list .word-item").length == 0) {
            return;
        }
        playing = !playing;
        $("#btn-toggle").text(!playing ? 'Start Practice' : 'Stop Practice');
        load_practice_word($("#word-list .word-item").eq(Math.floor(Math.random() * $("#word-list .word-item").length)).find(".word-item-text").text());
    });
});
function quiz_word() {
    var final_transcript = '';
    var recognition = new webkitSpeechRecognition();
   recognition.lang = 'zh-CN';
      // recognition.lang = 'cmn';
    recognition.onresult = function(event) {
        for (var i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
                if (event.results[i][0].transcript) {
                    final_transcript += event.results[i][0].transcript;
                }
            }
        }
        if (final_transcript) {
            console.log(final_transcript);
        }
    }
    recognition.start();
}

function process_input(inpt) {

}

function load_practice_word(word) {
    $("#practice-word").text(word);
}
