from flask import Flask,redirect,url_for
import os
def create_app():
    app = Flask(__name__)
    app.config["ENV"] = os.getenv("ICZ_ENV","development")
    app.config["DEBUG"] = os.getenv("ICZ_DEBUG",1)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("ICZ_DB","sqlite:///.data/data.db")
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 32
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["SECRET_KEY"]=str(os.urandom(20))
    app.jinja_env.line_statement_prefix='#'

    from .pages import events
    app.register_blueprint(events.bp)

    from .pages import staticFiles
    app.register_blueprint(staticFiles.bp)

    from . import db
    db.init_db(app)

    @app.route('/')
    def index():
        return redirect(url_for('events.list_posts'))

    return app