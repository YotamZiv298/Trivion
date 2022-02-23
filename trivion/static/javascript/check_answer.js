// Shorthand for $( document ).ready()
$(function() {
    console.log("ready!");
    $(".answer").on('click', function(){
        var answer_num = $(this).attr('id');
        $.ajax({
            url: '/game/assign_answer',
            //dataType: 'json',
            type: 'POST',
            contentType: 'application/json',
            data: get_answer(answer_num),
            success: function(data, textStatus, jQxhr) {
                //$('#response pre').html(data);
                // var obj = jQuery.parseJSON(data);
                if (data.success) {
                    change_page()
                    /*
                    if (data.ans) {
                        setTimeout(function(){  window.location.replace("/game" + "/" + document.getElementById("PIN").innerHTML + "/Correct") }, 5000);
                        setTimeout(function(){ window.history.back() }, 5000);
                    }
                    else {
                        setTimeout(function(){  window.location.replace("/game" + "/" + document.getElementById("PIN").innerHTML + "/Inorrect") }, 5000);
                        setTimeout(function(){ window.history.back() }, 5000);
                    }
                    */
                }
            },
            error: function(jqXhr, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    });
});

function get_answer(answer_num) {
    answer = {};

    answer["answer"] = answer_num;
    answer["game_pin"] = document.getElementById("PIN").innerHTML;

    js_str = JSON.stringify(answer);
    return js_str;
}

function change_page() {
    $(".change_after_click").remove();

    var base = document.getElementsByClassName("base");
    $(
    "<tr class='change_after_click'><td colspan='2'><center> <b style='font-size: 45px; font-family: sans-serif;'>Answered!</b></center></td></tr><tr class='change_after_click'><td colspan='2'><center><div class='spinner-border text-success' role='status'> <span style='size: 50px' class='sr-only'>Loading...</span></div></center></td></tr><tr class='change_after_click'><td colspan='2'><center> <b style='font-size: 45px; font-family: sans-serif;'>Waiting for results...</b></center></td></tr>"
    ).insertAfter(base);
    $("#answer_table").attr('width', 1100);
}