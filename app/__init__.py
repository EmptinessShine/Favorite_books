from flask import Flask, g, session, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os
from datetime import datetime

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(config_class)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
        instance_folder_for_db = os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'instance')
        os.makedirs(instance_folder_for_db, exist_ok=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except OSError:
        pass

    db.init_app(app)

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)

    from app.models import User

    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = User.query.get(user_id)
            if 'last_activity' in session:
                now = datetime.utcnow()
                try:

                    last_activity_time = datetime.fromisoformat(session['last_activity'])
                    if now > last_activity_time + app.config['PERMANENT_SESSION_LIFETIME']:
                        session.clear()
                        g.user = None
                        return
                except ValueError:
                    session['last_activity'] = now.isoformat()

            session['last_activity'] = datetime.utcnow().isoformat()


    @app.context_processor
    def inject_user_and_datetime():
        return dict(current_user=g.get('user', None), datetime=datetime)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    return app