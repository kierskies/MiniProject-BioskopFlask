from flask import Flask
from virtualcinema.db.database import db
from virtualcinema.accounts.accounts import account
from virtualcinema.films.films import film

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/VirtualCinema'
db.init_app(app)


app.register_blueprint(account)
app.register_blueprint(film)

if __name__ == '__main__':
    app.run()
