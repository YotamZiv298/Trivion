from trivion import create_app

HOST1 = "0.0.0.0"
HOST2 = "127.0.0.1"
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host=HOST1)

"""
All imports needed:
Flask
Flask-Bcrypt
Flask-Login
Flask-Mail
Flask-SQLAlchemy
Flask-WTF
Pillow 5.1.0
"""
