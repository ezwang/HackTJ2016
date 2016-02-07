var playing = false;
$(document).ready(function() {
    $("#add-word").click(function(e) {
        e.preventDefault();
        if (!$("#new-word-char").val()) {
            return;
        }
        $("#btn-toggle").prop("disabled", false);
        add_word($("<div />").text($("#new-word-char").val()).html(), $("<div />").text($("#new-word-trans").val()).html());
        $("#new-word-char, #new-word-trans").val("");
    });
    $("#new-word-char, #new-word-trans").keyup(function(e) {
        if (e.keyCode == 13) {
            $("#add-word").click();
        }
    });
    $("#word-list").on("click", ".word-item-delete", function(e) {
        e.preventDefault();
        var word = $(this).parent().find('.word-item-text').text();
        $(this).parent().remove();
        if ($("#word-list .word-item").length == 0) {
            $("#btn-toggle").prop("disabled", true);
        }
        $.get("/removeWord", "word=" + encodeURIComponent(word));
    });
    $("#btn-toggle").click(function(e) {
        e.preventDefault();
        if ($("#word-list .word-item").length == 0) {
            return;
        }
        playing = !playing;
        $("#btn-toggle").text(playing ? 'Stop Practice' : 'Start Practice');
        if (playing) {
            load_random_practice_word();
        }
        else {
            try {
                recognition.stop();
            }
            catch (e) { }
        }
    });
    $("#set-label").keyup(function(e) {
        if (e.keyCode == 13) {
            $("#load-set").click();
        }
    });
    $("#load-set").click(function(e) {
        e.preventDefault();
        $.getJSON('/loadSet', 'label=' + encodeURIComponent($('#set-label').val()), function(data) {
            $('#word-list').children().remove();
            if (data.data.length > 0) {
                $("#btn-toggle").prop("disabled", false);
            }
            $.each(data.data, function(k, v) {
                add_word(v[0], v[1]);
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
    $('#about-icon').click(function() {
      $('.about').slideDown('fast');
    });
    $('#about-div-bg, .x-button').click(function() {
      $('.about').css('display', 'none');
    });
    $('#speaker').click(function() {
        var chars = document.getElementById('practice-word').innerHTML;
        if (!chars) return;
        var audio = new Audio('/getTTS?chars=' + encodeURIComponent(chars));
        audio.play();
    });
    $("#upload-file").change(function(e) {
        if ($(this)[0].files.length > 0) {
            var selectedFile = $(this)[0].files[0];
            var read = new FileReader();
            read.readAsText(selectedFile, 'UTF-8');
            read.onloadend = function() {
                var data = read.result;
                $.each(data.split('\n'), function(k, v) {
                    if (v) {
                        var stuff = v.split('\t');
                        add_word(stuff[0], stuff[stuff.length-1]);
                    }
                });
                if (data) {
                    $("#btn-toggle").prop("disabled", false);
                }
            };
            $(this).val('');
        }
    });
});
function load_random_practice_word() {
    if (!playing) {
        $("#practice-word").text('');
        return;
    }
    load_practice_word($("#word-list .word-item").eq(Math.floor(Math.random() * $("#word-list .word-item").length)).find(".word-item-text").text(), $("#word-list .word-item").eq(Math.floor(Math.random() * $("#word-list .word-item").length)).find(".word-item-trans").text());
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
    $.get('/uni2pinyin', 'spoken=' + usrans + '&actual=' + $("#practice-word").data('word'), function(data) {
        if (data.toLowerCase() == "true") {
            $("#card-practice").css("background-color", "#4CAF50");
        }
        else {
            $("#card-practice").css("background-color", "#F44336");
        }
    });
    setTimeout(function() {
        $("#card-practice").css("background-color", "");
        load_random_practice_word();
    }, 3000);
}
function add_word(word, trans) {
    $('#word-list').append($("<div class='word-item'><span class='word-item-text'>" + word + "</span><span class='word-item-trans'>" + trans + "</span><span class='word-item-delete'>&times;</span></div>"));
    $.get("/addWord", "word=" + encodeURIComponent(word));
}
function load_practice_word(word, trans) {
    $("#practice-word").data('word', word);
    if ($("#quiz-type").is(":checked")) {
        $("#practice-word").text(trans);
    }
    else {
        $("#practice-word").text(word);
    }
    quiz_word();
}
