var q_counter = 1;
var start = 1;

function addQuestion() {
    q_counter++;
    if (q_counter <= 30) {
        createTable(q_counter);
    }
    if (q_counter == 30) {
        $("#add_q_button").remove();
    }
}

function createTable(q_counter) {
    var game_table = document.getElementById("game_table");

    var newRow = game_table.insertRow(game_table.rows.length - 1);
    var newCell = newRow.insertCell();
    var question_table = document.getElementById("question_table").innerHTML;

    newCell.innerHTML = question_table;

    var question_titles = document.getElementsByClassName("questions");
    question_titles[q_counter - 1].innerHTML = "Question " + q_counter + ":";
    question_titles[q_counter - 1].id = "question_num" + q_counter;
    question_titles[q_counter - 1].name = "question_num" + q_counter;

    var question_txt = document.getElementsByClassName("question");
    question_txt[q_counter - 1].id = "question" + q_counter;
    question_txt[q_counter - 1].name = "question" + q_counter;

    var question_answers_txt = document.getElementsByClassName("answers");
    for (var i = start; i < q_counter; i++)
        for (var j = 0; j < 4; j++)
        {
            question_answers_txt[i*4 + j].id = "answer_" + (j + 1) + "_" + (i + 1);
            question_answers_txt[i*4 + j].name = "answer_" + (j + 1) + "_" + (i + 1);
        }

    var question_answers = document.getElementsByClassName("bigradio");
    for (var i = start; i < q_counter; i++)
        for (var j = 0; j < 4; j++)
        {
            question_answers[i*4 + j].id = "question_answer_" + (j + 1) + "_" + (i + 1);
            question_answers[i*4 + j].name = "ans_" + (i + 1);
        }

    start = q_counter;
}

function create_json_game() {
    var question_titles = document.getElementsByClassName("questions");
    var question_txt;
    var question_answers_txt = document.getElementsByClassName("answers");
    var question_answers = document.getElementsByClassName("bigradio");

    game_obj = {};
    game_obj["Title"] = document.getElementById("title").value;
    question_arr = [];

    for (var i = 0; i < q_counter; i++) {
        question_obj = {};
        question_txt = document.getElementById("question" + (i + 1));

        question_obj["Question_Num"] = (question_titles[i].id).substr((question_titles[i].id).length - 1);
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
        ans = 1;
        question_arr[i] = question_obj;
    }

    game_obj["Question_Arr"] = question_arr;

    js_str = JSON.stringify(game_obj);
    return js_str;
}