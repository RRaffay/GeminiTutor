from flask import Flask, session


def create_app():
    app = Flask(__name__)
    app.secret_key = 'supersecretkey12345'

    from .main.routes import main
    from .auth.routes import auth

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    @app.context_processor
    def inject_logged_in():
        return {'logged_in': 'user_id' in session}

    return app
