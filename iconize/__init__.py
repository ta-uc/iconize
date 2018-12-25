from flask import Flask,redirect,url_for,render_template,request
from flask_sslify import SSLify
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os
from werkzeug.contrib.fixers import ProxyFix

def create_app():
    #pylint: disable=W0612
    app = Flask(__name__)
    app.config["ENV"] = os.getenv("ICZ_ENV","development")
    app.config["DEBUG"] = os.getenv("ICZ_DEBUG",1)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL","sqlite:///.data/data.db")
    app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 32
    app.config["PREFERRED_URL_SCHEME"] = "https"
    app.config["SECRET_KEY"]=os.getenv("SECRET",str(os.urandom(20)))
    app.jinja_env.line_statement_prefix='#'

    from .pages import events
    app.register_blueprint(events.bp)

    from .pages import staticFiles
    app.register_blueprint(staticFiles.bp)

    from . import db
    db.init_db(app)

    @app.route("/")
    def index():
        return redirect(url_for('events.list_posts'))

    @app.errorhandler(404)
    def page_not_found(err):
        return render_template('/err/404.html'), 404

    class icnzmodelview(ModelView):

        def is_accessible(self):
            if request.args.get("K") != os.getenv("ICZ_ADMINKEY") or os.getenv("ICZ_ADMINKEY") is None:
                return False
            else:
                return True

        can_create = False
        can_edit = False
        can_delete = False
        column_list=["iD","token","author","title","created_date","updated_date"]
        
    app.wsgi_app = ProxyFix(app.wsgi_app)
    sslify = SSLify(app)
    admin = Admin(app, name="Need Password", template_mode="bootstrap3")
    admin.add_view(icnzmodelview(db.Post,db.db.session))

    return app