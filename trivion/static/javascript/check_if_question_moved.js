// Shorthand for $( document ).ready()
$(function() {
    console.log("ready!");
    function checkIfQuestionMoved(e) {
        $.ajax({
            url: '/game/check_if_question_moved',
            //dataType: 'json',
            type: 'POST',
            contentType: 'application/json',
            data: create_json_game_pin(),
            success: function(data, textStatus, jQxhr) {
                //$('#response pre').html(data);
                // var obj = jQuery.parseJSON(data);
                if (data.success) {
                    if (data.correct) {
                        if (data.last) {
                            correct(run)
                            run ++;
                            setTimeout(function(){ window.location.replace("/home") }, 5000);
                            return;
                        }
                        else {
                            correct(run)
                            run ++;
                            setTimeout(function(){
                                window.location.replace("/game/" + document.getElementById("PIN").innerHTML + "/" + (Number(window.location.pathname.split('/')[3]) + 1) + "/PlayersAnswersPage");
                            }, 5000);
                        } 
                    }
                    else {
                        if (data.last) {
                            incorrect(run)
                            run ++;
                            setTimeout(function(){ window.location.replace("/home") }, 5000);
                            return;
                        }
                        else {
                            incorrect(run)
                            run ++;
                            setTimeout(function(){
                                window.location.replace("/game/" + document.getElementById("PIN").innerHTML + "/" + (Number(window.location.pathname.split('/')[3]) + 1) + "/PlayersAnswersPage");
                            }, 5000);
                        } 
                    }
                }
            },
            error: function(jqXhr, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    }
    var run = 1;
    $(".answer").on('click', checkIfQuestionMoved);
    var timer = setInterval(function(){ checkIfQuestionMoved() },500);
});

function create_json_game_pin() {
    data = {};

    data["game_pin"] = document.getElementById("PIN").innerHTML;
    data["current_question"] = window.location.pathname.split('/')[3];

    js_str = JSON.stringify(data);
    return js_str;
}

function correct(run) {
    if (run == 1) {
        $(".change_after_click").remove();

        var base = document.getElementsByClassName("base");
        $(
            "<tr><td colspan='2'><center><table border='0' cellpadding='15'><tr><td><center><b style='font-size: 40px; font-family: sans-serif; color: white'>Correct</b></center></td></tr><tr><td><center><img src='/static/correct.png'></center></td></tr><tr><td bgcolor='white'><center><b style='font-size: 20px; font-family: sans-serif;'>+100</b></center></td></tr></table></center></td></tr>"
        ).insertAfter(base);
    }
}

function incorrect(run) {
    if (run == 1) {
        $(".change_after_click").remove();

        var base = document.getElementsByClassName("base");
        $(
            "<tr><td colspan='2'><center><table border='0' cellpadding='15'><tr><td><center><b style='font-size: 40px; font-family: sans-serif; color: white'>Inorrect</b></center></td></tr><tr><td><center><img src='/static/wrong.png' height='76' width='80'></center></td></tr><tr><td bgcolor='white'><center><b style='font-size: 20px; font-family: sans-serif;'>No score :-(</b></center></td></tr></table></center></td></tr>"
        ).insertAfter(base);
    }
}