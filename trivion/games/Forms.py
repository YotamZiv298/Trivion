from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length


class EnterGameForm(FlaskForm):
    """
    Class for entering a game
    """
    game_pin = StringField("PIN", validators=[DataRequired(), Length(min=6, max=6,
                                                                     message="Field must be 6 characters long.")])
    nickname = StringField("nickname", validators=[DataRequired(), Length(min=2, max=20)])
    submit = SubmitField("Post")


class QuestionForm(FlaskForm):
    """
    Class for creating a game
    """
    title = StringField("Title", validators=[DataRequired()])
    question = StringField("Question", validators=[DataRequired()])
    answer1 = StringField("Answer1", validators=[DataRequired()])
    answer2 = StringField("Answer2", validators=[DataRequired()])
    answer3 = StringField("Answer3", validators=[DataRequired()])
    answer4 = StringField("Answer4", validators=[DataRequired()])
    ans = RadioField("ans", choices=[("1", "Triangle"), ("2", "Diamond"), ("3", "Circle"), ("4", "Square")])
    submit = SubmitField("Post")
