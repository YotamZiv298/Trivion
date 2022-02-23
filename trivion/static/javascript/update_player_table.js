// Shorthand for $( document ).ready()
$(function() {
    console.log("ready!");
    function updateTable(e) {
        $.ajax({
            url: '/game/update_player_table',
            //dataType: 'json',
            type: 'POST',
            contentType: 'application/json',
            data: create_json_game_pin(),
            success: function(data, textStatus, jQxhr) {
                //$('#response pre').html(data);
                // var obj = jQuery.parseJSON(data);
                if (data.success)
                    updateTableHTML(data.msg)
            },
            error: function(jqXhr, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
    }
    var timer = setInterval(function(){ updateTable() },500);
});

function create_json_game_pin() {
    pin = {};

    pin["game_pin"] = document.getElementById("PIN").innerHTML;

    js_str = JSON.stringify(pin);
    return js_str;
}

function updateTableHTML(players) {
    var row = document.getElementById("PlayersList");
    row_len = row.cells.length;

    document.getElementById("counter").innerHTML = row_len;

    for (var i = 0; i < row_len; i++)
        row.deleteCell(0);
    
    for (var i = 0; i < players.length; i++) {
        var x = row.insertCell(0);

        var b_tag = document.createElement("b");
        var name = document.createTextNode(players[i]["name"]);
        b_tag.appendChild(name);
        b_tag.style.cssText = "font-family: sans-serif; font-size: 20px; color: white";
        x.appendChild(b_tag);
    }
}