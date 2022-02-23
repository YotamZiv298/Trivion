// Shorthand for $( document ).ready()
$(function() {
    console.log("ready!");
    function checkIfGameStarted(e) {
        $.ajax({
            url: '/game/check_if_game_started',
            //dataType: 'json',
            type: 'POST',
            contentType: 'application/json',
            data: create_json_game_pin(),
            success: function(data, textStatus, jQxhr) {
                //$('#response pre').html(data);
                // var obj = jQuery.parseJSON(data);
                if (data.success)
                    window.location.replace("/game/" + document.getElementById("PIN").innerHTML + "/" + "1" + "/PlayersAnswersPage");
            },
            error: function(jqXhr, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    }
    var timer = setInterval(function(){ checkIfGameStarted() },500);
});

function create_json_game_pin() {
    pin = {};

    pin["game_pin"] = document.getElementById("PIN").innerHTML;

    js_str = JSON.stringify(pin);
    return js_str;
}