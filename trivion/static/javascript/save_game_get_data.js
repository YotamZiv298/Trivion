function get_form_data() {
    var question_titles = document.getElementsByClassName("questions");
    var question_txt;
    var question_answers_txt = document.getElementsByClassName("answers");
    var question_answers = document.getElementsByClassName("bigradio");
    var question_delete = document.getElementsByClassName("bigcheckbox");

    game_obj = {};
    game_obj["Title"] = document.getElementById("title").value;
    question_arr = [];

    for (var i = 0; i < question_titles.length; i++) {
        question_obj = {};
        question_txt = document.getElementById("question" + (i + 1));

        question_obj["Question_Num"] = (question_txt.id).substr((question_txt.id).length - 1);
        question_obj["Question"] = question_txt.value;
        question_obj["Answer1"] = question_answers_txt[i*4].value;
        question_obj["Answer2"] = question_answers_txt[i*4 + 1].value;
        question_obj["Answer3"] = question_answers_txt[i*4 + 2].value;
        question_obj["Answer4"] = question_answers_txt[i*4 + 3].value;
        var ans = 1;
        for (var j = 0; j < 4; j++) {
            if (question_answers[i*4 + j].checked) {
                    question_obj["Ans"] = ans;
                    break;
            }
            ans++;
        }
        if (question_delete[i].checked)
            question_obj["Delete"] = 1;
        else
            question_obj["Delete"] = 0;

        ans = 1;
        question_arr[i] = question_obj;
    }

    game_obj["Question_Arr"] = question_arr;

    js_str = JSON.stringify(game_obj);
    return js_str;
}