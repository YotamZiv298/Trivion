from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from trivion import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Class for user model in data base
    """
    u_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(16), nullable=False)

    game = db.relationship("Game", backref="name", lazy=True)

    def get_id(self):
        return self.u_id

    def get_reset_token(self, expires_sec=1800):
        """
        Creates a reset token
        :param expires_sec: how many seconds the token will be available
        :return: dumped token
        """
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.u_id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        """
        Check if the token is the same one
        :param token: token
        :return: user id
        """
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Game(db.Model):
    """
    Class for game model in data base
    """
    g_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.u_id"), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    questions = db.relationship("Questions", lazy=True)

    def get_id(self):
        return self.g_id

    def __repr__(self):
        return f"Game('{self.title}', '{self.user_id}', '{self.date_created}')"


class Questions(db.Model):
    """
    Class for questions model in data base
    """
    q_id = db.Column(db.Integer, primary_key=True)
    g_id = db.Column(db.Integer, db.ForeignKey("game.g_id"), nullable=False)
    question_number = db.Column(db.Integer, nullable=False)
    question = db.Column(db.String(120), nullable=False)
    answer1 = db.Column(db.String(75), nullable=False)
    answer2 = db.Column(db.String(75), nullable=False)
    answer3 = db.Column(db.String(75), nullable=False)
    answer4 = db.Column(db.String(75), nullable=False)
    ans = db.Column(db.Integer, nullable=False)

    def get_id(self):
        return self.g_id

    def __repr__(self):
        return f"Questions('{self.g_id}', '{self.question}')"


class Play(db.Model):
    play_id = db.Column(db.Integer, primary_key=True)
    game_pin = db.Column(db.String(6), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.g_id"), nullable=False)
    number_of_questions = db.Column(db.Integer, nullable=False)
    timer = db.Column(db.Integer, nullable=False)
    randomized = db.Column(db.Boolean, nullable=False)
    game_started = db.Column(db.Boolean, nullable=False)
    current_question = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Play('{self.play_id}', '{self.game_pin}', '{self.game_started}')"


class Ranking(db.Model):
    rank_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.u_id"), nullable=False)
    nickname = db.Column(db.String(20), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.g_id"), nullable=False)
    game_pin = db.Column(db.String(6), db.ForeignKey("play.game_pin"), nullable=False)
    current_answer = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Ranking('{self.rank_id}', '{self.user_id}', '{self.nickname}', '{self.points}')"
