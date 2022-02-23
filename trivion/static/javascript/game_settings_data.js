function get_settings_data() {
    game_obj = {}

    var timer = document.getElementById("timer");
    var timer_value = timer.options[timer.selectedIndex].value;
    game_obj["Timer"] = timer_value;

    var randomize_order = false;
    if (document.getElementById("randomize_order").checked)
        randomize_order = true;
    game_obj["Random"] = randomize_order;

    js_str = JSON.stringify(game_obj);
    return js_str;
}