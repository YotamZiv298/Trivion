from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from trivion.Models import User


class LoginForm(FlaskForm):
    """
    Class for log in form
    """
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=10)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=16)])
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    """
    Class for registration form
    """
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=16)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """
        Checks if username is already taken
        :param username: username
        :return: if exists raise error
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already taken, choose a different one.")

    def validate_email(self, email):
        """
        Checks if email is already taken
        :param email: email
        :return: if exists raise error
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is already taken, choose a different one.")


class UpdateAccountForm(FlaskForm):
    """
    Class for updating account info
    """
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=10)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        """
        Checks if username is different from current one and if it is already taken
        :param username: username
        :return: if exists raise error
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is already taken, choose a different one.")

    def validate_email(self, email):
        """
        Checks if email is different from current one and if it is already taken
        :param email
        :return: if exists raise error
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email is already taken, choose a different one.")


class RequestResetForm(FlaskForm):
    """
    Class for request to reset password
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """
        Checks if email exists
        :param email
        :return: if does not exists raise error
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")


class ResetPasswordForm(FlaskForm):
    """
    Class for resetting password
    """
    password = PasswordField("Password", validators=[DataRequired(), Length(min=2, max=16)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset Password")
