import os
from flask import Flask,render_template
from flask_login import current_user
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

def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db,User=User,Photo=Photo,Tag=Tag,
                    Follow=Follow,Collect=Collect,Comment=Comment,
                    Notification=Notification)

def register_template_context(app):
    @app.context_processor
    def make_template_context():
        if current_user.is_authenticated:
            notification_count=Notification.query.with_parent(current_user).filter_by(is_read=False).count()
        else:
            notification_count=None
        return dict(notification_count=notification_count)

def register_errorhandlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'),400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'),403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'),404

    @app.errorhandler(413)
    def request_entity_too_large(e):
        return render_template('errors/413.html'),413

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'),500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html',description=e.descripition),500