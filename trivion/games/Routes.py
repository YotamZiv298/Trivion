from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint, jsonify, Response)
from flask_login import current_user, login_required
from trivion import db
from trivion.Models import User, Questions, Game, Play, Ranking
from trivion.games.Forms import QuestionForm, EnterGameForm
from random import randint

games = Blueprint("games", __name__)

GET = "GET"
POST = "POST"

CREATE_GAME = "CreateGame.html"
LOAD_GAME = "LoadGame.html"
UPDATE_GAME = "UpdateGame.html"
GAME = "Game.html"
LOBBY = "Lobby.html"
GAME_SETTINGS = "GameSettings.html"
QUESTION = "Question.html"
RESULTS = "Results.html"
LEADER_BOARD = "Leaderboard.html"
ENTER_GAME = "EnterGame.html"
WAITING = "Waiting.html"
PLAYERS_ANSWERS_PAGE = "PlayersAnswersPage.html"
ANSWERED_CORRECT = "AnsweredRight.html"
ANSWERED_INCORRECT = "AnsweredWrong.html"


@games.route("/game/<int:game_id>/lobby", methods=[GET, POST])
@login_required
def lobby(game_id):
    """
    Lobby page route
    :param game_id: id of the game
    :return: Lobby.html template
    """
    game = Game.query.get_or_404(game_id)
    pin = randint(111111, 999999)
    number_of_questions = 0
    for i in Questions.query.filter_by(g_id=game_id).all():
        number_of_questions += 1
    play = Play(game_pin=pin, game_id=game.g_id, number_of_questions=number_of_questions,
                timer=0, randomized=False, game_started=False, current_question=0)
    db.session.add(play)
    db.session.commit()
    return render_template(LOBBY, title="Lobby", PIN=pin, game=game)


@games.route("/game/<int:game_id>/<int:game_pin>/settings", methods=[GET, POST])
@login_required
def game_settings(game_id, game_pin):
    """
    Game settings page route
    :param game_id: id of the game
    :param game_pin: pin code of the game
    :return: GameSettings.html template
    """
    req = request.get_json()
    if req is not None:
        play = Play.query.filter_by(game_pin=game_pin).first()
        play.timer = req["Timer"]
        play.randomized = req["Random"]
        try:
            db.session.commit()
            return jsonify(success=1, timer=req["Timer"], game_pin=str(game_pin))
        except:
            return jsonify(success=0)
    else:
        game = Game.query.get_or_404(game_id)
        return render_template(GAME_SETTINGS, title="Game Settings", game=game)


@games.route("/game/<int:game_id>/start", methods=[GET, POST])
@login_required
def start(game_id):
    """
    Start game
    :param game_id: id of the game
    """
    Play.query.filter_by(game_pin=int(request.args["game_pin"])).first().game_started = True
    db.session.commit()
    question_number = 0
    return redirect(url_for('games.question_display', game_id=game_id, game_pin=int(request.args["game_pin"]),
                            question_number=question_num_up(question_number, game_id), timer=request.args["timer"]))


def question_num_up(question_number, game_id):
    question_number += 1
    return question_number


@games.route("/game/<int:game_id>/<int:game_pin>/question<int:question_number>/<string:timer>", methods=[GET, POST])
@login_required
def question_display(game_id, game_pin, question_number, timer):
    """
    Question display page
    :param game_id: id of the game
    :param game_pin: pin code of the game
    :param question_number: number of question
    :param timer: timer
    :return: Question.html template
    """
    question = Questions.query.filter_by(g_id=game_id, question_number=question_number).first()
    Play.query.filter_by(game_pin=game_pin).first().current_question = question_number
    db.session.commit()
    if question is None:
        return redirect(url_for("games.leader_board", game_id=game_id, game_pin=game_pin))
    return render_template(QUESTION, title="Question " + str(question_number), question=question, timer=timer,
                           game_id=game_id, game_pin=game_pin)


@games.route("/game/<int:game_id>/<int:game_pin>/question<int:question_number>/results", methods=[GET, POST])
@login_required
def results(game_id, game_pin, question_number):
    """
    Results page
    :param game_id: id of the game
    :param game_pin: pin code of the game
    :param question_number: number of question
    :return: Results.html template
    """
    Play.query.filter_by(game_pin=game_pin).first().current_question = question_number + 1
    db.session.commit()

    answer_counter = [0, 0, 0, 0]
    for p in Ranking.query.filter_by(game_pin=game_pin).all():
        try:
            p = p.__dict__
            if p["current_answer"] == 1:
                answer_counter[0] += 1
            elif p["current_answer"] == 2:
                answer_counter[1] += 1
            elif p["current_answer"] == 3:
                answer_counter[2] += 1
            elif p["current_answer"] == 4:
                answer_counter[3] += 1
        except:
            Ranking.query.get_or_404(game_pin)
    answer_counter.append(
        {"correct_ans": [Questions.query.filter_by(g_id=game_id, question_number=question_number).first().ans]}
    )
    answer_counter[4]["correct_ans"]\
        .append(get_answer_text(game_id, answer_counter[4]["correct_ans"][0], question_number))
    return render_template(RESULTS, title="Q" + str(question_number) + " Results", game_pin=game_pin,
                           question_number=question_number, timer=request.args["timer"],
                           game_id=game_id, answer_counter=answer_counter,
                           player_table_scores=score_table_sort(game_pin))


def get_answer_text(game_id, ans_num, question_number):
    if ans_num == 1:
        return Questions.query.filter_by(g_id=game_id, question_number=question_number).first().answer1
    elif ans_num == 2:
        return Questions.query.filter_by(g_id=game_id, question_number=question_number).first().answer2
    elif ans_num == 3:
        return Questions.query.filter_by(g_id=game_id, question_number=question_number).first().answer3
    else:
        return Questions.query.filter_by(g_id=game_id, question_number=question_number).first().answer4


def score_table_sort(game_pin):
    names_and_score = []
    for p in Ranking.query.filter_by(game_pin=game_pin).all():
        try:
            p = p.__dict__
            data = {"name": p["nickname"], "score": p["points"]}
            names_and_score.append(data)
        except:
            Ranking.query.get_or_404(game_pin)
    names_and_score = sorted(names_and_score, key=lambda k: k["score"], reverse=True)
    return names_and_score


@games.route("/game/<int:game_id>/<int:game_pin>/leaderboard", methods=[GET, POST])
@login_required
def leader_board(game_id, game_pin):
    """
    Leaderboard page
    :param game_id: id of the game
    :param game_pin: pin code of the game
    :return: Leaderboard.html template
    """
    return render_template(LEADER_BOARD, title="Leader Board", game_id=game_id,
                           game_pin=game_pin, data=score_table_sort(game_pin))


@games.route("/game/save", methods=[GET, POST])
@login_required
def save_game():
    """
    Save new game
    """
    req = request.get_json()
    title = req["Title"]
    game = Game(title=title, name=current_user)
    db.session.add(game)
    db.session.flush()

    for i in range(0, len(req["Question_Arr"])):
        try:
            question_num = req["Question_Arr"][i]["Question_Num"]
            question = req["Question_Arr"][i]["Question"]
            answer1 = req["Question_Arr"][i]["Answer1"]
            answer2 = req["Question_Arr"][i]["Answer2"]
            answer3 = req["Question_Arr"][i]["Answer3"]
            answer4 = req["Question_Arr"][i]["Answer4"]
            ans = req["Question_Arr"][i]["Ans"]
            questions = Questions(g_id=game.g_id, question_number=question_num, question=question, answer1=answer1,
                                  answer2=answer2, answer3=answer3, answer4=answer4, ans=ans)
            db.session.add(questions)
        except:
            msg = flash("Failed to create your game", "danger")
            return jsonify(success=0, msg=msg)
    db.session.commit()
    msg = flash("Your game has been created", "success")
    return jsonify(success=1, msg=msg)


@games.route("/game/new", methods=[GET, POST])
@login_required
def new_game():
    """
    New game page route
    :return: CreateGame.html template
    """
    form = QuestionForm()
    if form.validate_on_submit():
        return redirect(url_for("main.home"))
    return render_template(CREATE_GAME, title="New Game", form=form, legend="New Game")


@games.route("/game/load")
@login_required
def load_game():
    """
    Load game page route
    :return: LoadGame.html template
    """
    page = request.args.get("page", 1, type=int)
    games = Game.query.order_by(Game.date_created.desc()).paginate(page=page, per_page=5)
    return render_template(LOAD_GAME, title="Load Game", games=games)


@games.route("/game/<int:game_id>")
@login_required
def game(game_id):
    """
    Specific game page route
    :param game_id: id of the game
    :return: Game.html
    """
    game = Game.query.get_or_404(game_id)
    questions = [game.title]

    for u in Questions.query.filter_by(g_id=game_id).all():
        try:
            u = u.__dict__
            question = \
                {"Question_Num": u["question_number"], "Question": u["question"], "Answer1": u["answer1"],
                 "Answer2": u["answer2"], "Answer3": u["answer3"], "Answer4": u["answer4"], "Ans": u["ans"]}
            questions.append(question)
        except:
            Questions.query.get_or_404(game_id)
    return render_template(GAME, title=game.title, game=game, questions=questions)


@games.route("/game/<int:game_id>/download")
@login_required
def game_download(game_id):
    """
    Download game to csv file
    """
    game = Game.query.get_or_404(game_id)
    questions = [game.title]

    for u in Questions.query.filter_by(g_id=game_id).all():
        try:
            u = u.__dict__
            question = \
                {"Question_Num": u["question_number"], "Question": u["question"], "Answer1": u["answer1"],
                 "Answer2": u["answer2"], "Answer3": u["answer3"], "Answer4": u["answer4"], "Ans": u["ans"]}
            questions.append(question)
        except:
            Questions.query.get_or_404(game_id)
    csv = f"{questions[0]}, Question, Answer 1, Answer 2, Answer 3, Answer 4, True answer\n"
    for u, i in zip(questions, range(1, len(questions))):
        csv += str(questions[i]["Question_Num"]).replace(",", " ")
        csv += ","
        csv += str(questions[i]["Question"]).replace(",", " ")
        csv += ","
        csv += str(questions[i]["Answer1"]).replace(",", " ")
        csv += ","
        csv += str(questions[i]["Answer2"]).replace(",", " ")
        csv += ","
        csv += str(questions[i]["Answer3"]).replace(",", " ")
        csv += ","
        csv += str(questions[i]["Answer4"]).replace(",", " ")
        csv += ","
        csv += str(questions[i]["Ans"])
        csv += "\n"
    csv += f"Created by: {User.query.filter_by(u_id=game.user_id).first().username}"
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={questions[0]}.csv"})


@games.route("/game/<int:game_id>/update", methods=[GET, POST])
@login_required
def update_game(game_id):
    """
    Update game page route
    :param game_id: id of the game
    :return: updated game
    """
    form = QuestionForm()
    game = Game.query.get_or_404(game_id)
    if game.name != current_user:
        abort(403)
    questions = []
    try:
        req = request.get_json()
        if req is not None:
            game.title = req["Title"]
            questions.append(req["Title"])
            num_of_question_to_delete = []
            for u, i in zip(Questions.query.filter_by(g_id=game_id).all(), range(0, len(req["Question_Arr"]))):
                u.question_num = req["Question_Arr"][i]["Question_Num"]
                u.question = req["Question_Arr"][i]["Question"]
                u.answer1 = req["Question_Arr"][i]["Answer1"]
                u.answer2 = req["Question_Arr"][i]["Answer2"]
                u.answer3 = req["Question_Arr"][i]["Answer3"]
                u.answer4 = req["Question_Arr"][i]["Answer4"]
                u.ans = req["Question_Arr"][i]["Ans"]
                if req["Question_Arr"][i]["Delete"]:
                    num_of_question_to_delete.append(req["Question_Arr"][i]["Question_Num"])
            delete_question(game_id, num_of_question_to_delete)
            db.session.commit()
            msg = flash("Your game has been updated", "success")
            return jsonify(success=1, msg=msg)
    except:
        msg = flash("Failed to update your game", "danger")
        return jsonify(success=0, msg=msg)
    if request.method == GET:
        questions.append(game.title)
        for u in Questions.query.filter_by(g_id=game_id).all():
            try:
                u = u.__dict__
                question = \
                    {"Question_Num": u["question_number"], "Question": u["question"], "Answer1": u["answer1"],
                     "Answer2": u["answer2"], "Answer3": u["answer3"], "Answer4": u["answer4"], "Ans": u["ans"]}
                questions.append(question)
            except:
                Questions.query.get_or_404(game_id)
        return render_template(UPDATE_GAME, title=game.title, game=game,
                               questions=questions, form=form, game_id=game_id)


def delete_question(game_id, num_of_question_to_delete):
    for i in num_of_question_to_delete:
        Questions.query.filter_by(g_id=game_id, question_number=i).delete()
    num = 0
    for i in Questions.query.filter_by(g_id=game_id).all():
        num += 1
    for q, i in zip(Questions.query.filter_by(g_id=game_id).all(), range(1, (num + 1))):
        q.question_number = i


@games.route("/game/<int:game_id>/delete", methods=[POST])
@login_required
def delete_game(game_id):
    """
    Delete game route
    :param game_id: id of the game
    :return: Home.html
    """
    game = Game.query.get_or_404(game_id)
    if game.name != current_user:
        abort(403)
    Questions.query.filter_by(g_id=game_id).delete()
    db.session.delete(game)
    db.session.commit()
    flash("Your game has been deleted", "success")
    return redirect(url_for("main.home"))


@games.route("/enter_game", methods=[GET, POST])
@login_required
def enter_game():
    """
    Enter game page
    :return: EnterGame.html template
    """
    form = EnterGameForm()
    if form.validate_on_submit():
        play = Play.query.filter_by(game_pin=form.game_pin.data).first()
        if play is not None:
            db.session.add(Ranking(user_id=current_user.u_id, nickname=form.nickname.data, game_id=play.game_id,
                                   game_pin=form.game_pin.data, current_answer=0, points=0))
            db.session.commit()
            return redirect(url_for("games.waiting", game_id=play.game_id, game_pin=play.game_pin))
    return render_template(ENTER_GAME, title="Enter Game", form=form)


@games.route("/game/<int:game_id>/<int:game_pin>/waiting", methods=[GET, POST])
@login_required
def waiting(game_id, game_pin):
    """
    Waiting room
    :param game_id: id of the game
    :param game_pin: pin code of the game
    :return: Waiting.html template
    """
    return render_template(WAITING, title="Waiting for the game to start...", PIN=game_pin)


@games.route("/game/check_if_game_started", methods=[GET, POST])
@login_required
def check_if_game_started():
    """
    Checking if the game started
    :return: Yes if started, no if not
    """
    req = request.get_json()
    if Play.query.filter_by(game_pin=req["game_pin"]).first().game_started:
        return jsonify(success=1)
    return jsonify(success=0)


@games.route("/game/<int:game_pin>/<int:question_num>/PlayersAnswersPage", methods=[GET, POST])
@login_required
def players_answers_page(game_pin, question_num):
    """
    Player's answers page
    :param game_pin: pin code of the game
    :param question_num: number of question
    :return: PlayersAnswersPage.html template
    """
    rank = Ranking.query.filter_by(game_pin=game_pin, user_id=current_user.u_id).first()
    number_of_questions = 0
    for i in Questions.query.filter_by(g_id=rank.game_id).all():
        number_of_questions += 1
    if question_num <= number_of_questions:
        return render_template(PLAYERS_ANSWERS_PAGE, title="Answer now", game_pin=game_pin, nickname=rank.nickname,
                               points=rank.points, question_num=question_num, number_of_questions=number_of_questions,
                               question=Questions.query.filter_by(g_id=rank.game_id, question_number=question_num)
                               .first())
    return redirect(url_for("main.home"))


@games.route("/game/<int:game_pin>/Correct", methods=[GET, POST])
@login_required
def correct(game_pin):
    """
    Correct screen
    :param game_pin: pin code of the game
    :return: Correct.html template
    """
    return render_template(ANSWERED_CORRECT, title="Correct")


@games.route("/game/<int:game_pin>/Incorrect", methods=[GET, POST])
@login_required
def incorrect(game_pin):
    """
    Incorrect screen
    :param game_pin: pin code of the game
    :return: Incorrect.html template
    """
    return render_template(ANSWERED_INCORRECT, title="Incorrect")


@games.route("/game/update_player_table", methods=[GET, POST])
@login_required
def update_players_table():
    """
    Update players table
    """
    req = request.get_json()
    if req is not None:
        names = []
        for p in Ranking.query.filter_by(game_pin=req["game_pin"]).all():
            try:
                p = p.__dict__
                name = {"name": p["nickname"]}
                names.append(name)
            except:
                Ranking.query.get_or_404(req["game_pin"])
        if names:
            return jsonify(success=1, msg=names)
    return jsonify(success=0)


@games.route("/game/assign_answer", methods=[GET, POST])
@login_required
def assign_answer():
    """
    Assign answer of player
    """
    req = request.get_json()
    if req is not None:
        Ranking.query.filter_by(user_id=current_user.u_id, game_pin=int(req["game_pin"])).first()\
            .current_answer = int(req["answer"])
        db.session.commit()
        real_ans = \
            Questions.query.filter_by(g_id=Play.query.filter_by(game_pin=int(req["game_pin"])).first().game_id,
                                      question_number=Play.query.filter_by(game_pin=int(req["game_pin"])).first()
                                      .current_question).first().ans
        if Ranking.query.filter_by(user_id=current_user.u_id, game_pin=int(req["game_pin"])).first().current_answer\
                == real_ans:
            Ranking.query.filter_by(user_id=current_user.u_id, game_pin=int(req["game_pin"])).first().points += 100
            db.session.commit()
            return jsonify(success=1, ans=1)
        return jsonify(success=1, ans=0)
    return jsonify(success=0)


@games.route("/game/check_if_question_moved", methods=[GET, POST])
@login_required
def check_if_question_moved():
    """
    Checking if question moved
    """
    req = request.get_json()
    correct = False
    if Questions.query.filter_by(g_id=Play.query.filter_by(game_pin=req["game_pin"]).first().game_id,
                                 question_number=req["current_question"]).first().ans == \
            Ranking.query.filter_by(game_pin=req["game_pin"], user_id=current_user.u_id).first().current_answer:
        correct = True
    if Play.query.filter_by(game_pin=req["game_pin"]).first().current_question > int(req["current_question"]):
        return jsonify(success=1, last=0, correct=correct)
    elif int(req["current_question"]) > Play.query.filter_by(game_pin=req["game_pin"]).first().number_of_questions:
        return jsonify(success=1, last=1, correct=correct)
    else:
        return jsonify(success=0)
