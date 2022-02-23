// Shorthand for $( document ).ready()
$(function() {
    console.log("ready!");
    function processForm(e) {
        $.ajax({
            url: '/game/save',
            //dataType: 'json',
            type: 'POST',
            contentType: 'application/json',
            data: create_json_game(),
            success: function(data, textStatus, jQxhr) {
                //$('#response pre').html(data);
                // var obj = jQuery.parseJSON(data);
                if (data.success) {
                    window.location.replace("/home");
                    $('#notice-flash').message(data.msg)
                }
                else {
                    $('#notice-flash').message(data.msg)
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
$('#save_game').submit(processForm);
});