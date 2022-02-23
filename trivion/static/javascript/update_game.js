// Shorthand for $( document ).ready()
$(function() {
    console.log("ready!");
    function processForm(e) {
        $.ajax({
            url: '/game/' + window.location.pathname.split('/')[2] + '/update',
            //dataType: 'json',
            type: 'POST',
            contentType: 'application/json',
            data: get_form_data(),
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
$('#update_game').submit(processForm);
});