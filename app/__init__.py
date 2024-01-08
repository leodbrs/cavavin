import os
from urllib.parse import quote

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FLASK_APP_SECRET_KEY", "")

# Constructing the database URI using environment variables
db_host = os.environ.get("MYSQL_HOST", "")
db_port = os.environ.get("MYSQL_PORT", 3306)
db_name = os.environ.get("MYSQL_NAME", "cavavin")
db_password = os.environ.get("MYSQL_ROOT_PASSWORD", "")

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"mysql://root:{quote(db_password)}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "auth.login"

from app.models import User  # noqa: E402


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def test_db_connection():
    with app.app_context():
        try:
            # Try to connect to the database
            db.session.execute(text("SELECT 1"))
            print("Database connection successful.")
        except OperationalError as e:
            # Handle connection error
            print(e.orig.args[1].split("(")[0])
            exit(1)


test_db_connection()

from app.views.auth import auth  # noqa: E402
from app.views.bottle_views import bottle  # noqa: E402
from app.views.cellar_views import cellar  # noqa: E402
from app.views.main import main  # noqa: E402
from app.views.rating_views import rating  # noqa: E402
from app.views.shelf_views import shelf  # noqa: E402
from app.views.user_views import user  # noqa: E402
from app.views.wine_views import wine  # noqa: E402

app.register_blueprint(rating)
app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(bottle)
app.register_blueprint(cellar)
app.register_blueprint(shelf)
app.register_blueprint(user)
app.register_blueprint(wine)

from app.error import *  # noqa: E402, F403
