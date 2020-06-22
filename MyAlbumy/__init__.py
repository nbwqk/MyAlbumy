import os
from flask import Flask
from MyAlbumy.extensions import bootstrap,moment,mail,db,login_manage,dropzone,whooshee,avatars,csrf
from MyAlbumy.settings import config
from MyAlbumy.blueprints.admin import admin_bp
from MyAlbumy.blueprints.ajax import ajax_bp
from MyAlbumy.blueprints.auth import auth_bp
from MyAlbumy.blueprints.main import main_bp
from MyAlbumy.blueprints.user import user_bp

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('MyAlbumy')

    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)

    return app

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    login_manage.init_app(app)
    mail.init_app(app)
    dropzone.init_app(app)
    moment.init_app(app)
    whooshee.init_app(app)
    csrf.init_app(app)

def register_blueprints(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp,url_prefix='/user')
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(ajax_bp, url_prefix='/ajax')