$(document).ready(function() {
    $("#add-word").click(function(e) {
        e.preventDefault();
        if (!$("#new-word-char").val()) {
            return;
        }
        $("#btn-toggle").prop("disabled", false);
        $("#word-list").append($("<div class='word-item'><span class='word-item-text'>" + $("<div />").text($("#new-word-char").val()).html() + "</span><span class='word-item-trans'>" + $("<div />").text($("#new-word-trans").val()).html() + "</span><span class='word-item-delete'>&times;</span></div>"));
        $("#new-word-char, #new-word-trans").val("");
    });
    $("#new-word-char, #new-word-trans").keyup(function(e) {
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
    $("#load-set").click(function(e) {
        e.preventDefault();
        $.getJSON('/loadSet', 'label=' + encodeURIComponent($('#set-label').val()), function(data) {
            $('#word-list').children().remove();
            if (data.data.length > 0) {
                $("#btn-toggle").prop("disabled", false);
            }
            $.each(data.data, function(k, v) {
                $('#word-list').append($("<div class='word-item'><span class='word-item-text'>" + v[0] + "</span><span class='word-item-trans'>" + v[1] + "</span><span class='word-item-delete'>&times;</span></div>"));
            });
        });
    });
    $("#save-set").click(function(e) {
        e.preventDefault();
        var words = [];
        $.each($("#word-list").children(), function(k, v) {
            words.push([$(this).find('.word-item-text').text(), $(this).find('.word-item-trans').text()]);
        });
        $.get('/saveSet', 'label=' + encodeURIComponent($('#set-label').val()) + '&words=' + encodeURIComponent(JSON.stringify(words)));
    });
    $("#delete-set").click(function(e) {
        e.preventDefault();
        $.get('/deleteSet', 'label=' + encodeURIComponent($('#set-label').val()));
    });
    $("#set-label").keyup(function(e) {
        $("#load-set, #save-set, #delete-set").prop("disabled", $("#set-label").val().length == 0);
    });
    $.get('/getListOfSets', function(data) {
      $('#set-label').autocomplete({source: data.data, delay: 0});
    });
    $('#upload-button').click(function(e) {
      $('#upload').slideDown('fast');
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
        check_answer(final_transcript);
    }
    recognition.start();
}
function check_answer(usrans) {
    $.get('/uni2pinyin', 'spoken=' + usrans + '&actual=' + $("#practice-word").text(), function(data) {
        if (data.toLowerCase() == "true") {
            $("#practice-word").css("background-color", "green");
        }
        else {
            $("#practice-word").css("background-color", "red");
        }
    });
    setTimeout(function() {
        $("#practice-word").css("background-color", "");
        load_random_practice_word();
    }, 3000);
}
function load_practice_word(word) {
    $("#practice-word").text(word);
    quiz_word();
}
