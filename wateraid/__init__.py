from flask import Flask
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from wateraid.config import Config

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users_blueprint.login'


def create_app(config_class=Config):
    """ Create the Flask application and register blueprints corresponding to each page """
    app = Flask(__name__)
    app.config.from_object(Config)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    client = MongoClient("mongodb://localhost:27017")
    client = MongoClient()

    from wateraid.users.routes import users_blueprint
    from wateraid.main.routes import main_blueprint
    from wateraid.search.routes import search_blueprint
    from wateraid.trends.routes import trends_blueprint
    from wateraid.article.routes import article_blueprint
    from wateraid.account.routes import account_blueprint
    from wateraid.errors.errors import errors

    app.register_blueprint(users_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(search_blueprint)
    app.register_blueprint(trends_blueprint)
    app.register_blueprint(article_blueprint)
    app.register_blueprint(account_blueprint)
    app.register_blueprint(errors)

    return app
