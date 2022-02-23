from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from trivion.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    """
    create app
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from trivion.users.Routes import users
    from trivion.games.Routes import games
    from trivion.main.Routes import main
    from trivion.errors.Handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(games)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
