class Config:
    """
    Need to login to email to turn on access for python to send email before usage
    """
    SECRET_KEY = "d2c13b0ed9c56019d1c76b63ad53530d"
    SQLALCHEMY_DATABASE_URI = "sqlite:///Site.db"
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "" # Email address
    MAIL_PASSWORD = "" # Email password
