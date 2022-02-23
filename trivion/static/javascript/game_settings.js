// Shorthand for $( document ).ready()
$(function() {
    console.log("ready!");
    function processForm(e) {
        $.ajax({
            url: '/game/' + window.location.pathname.split('/')[2] + '/' + window.location.pathname.split('/')[3] + '/settings',
            //dataType: 'json',
            type: 'POST',
            contentType: 'application/json',
            data: get_settings_data(),
            success: function(data, textStatus, jQxhr) {
                //$('#response pre').html(data);
                // var obj = jQuery.parseJSON(data);
                if (data.success) {
                    window.location.replace("/game/" + window.location.pathname.split('/')[2] + "/start" + "?timer=" + data["timer"] + "&game_pin=" + data["game_pin"]);
                }
                console.log("Sucess:" + data.msg);
            },
            error: function(jqXhr, textStatus, errorThrown) {
                console.log(errorThrown);
            }
        });
        // Stop the form from submitting the normal way and refreshing the page
        e.preventDefault();
    }
$('#game_settings').submit(processForm);
});