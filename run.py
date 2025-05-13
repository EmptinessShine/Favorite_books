from app import create_app, db
from app.models import User, Book
import os

app = create_app()

if __name__ == '__main__':
    instance_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'instance')
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with app.app_context():
        db.create_all()
        print(f"Database will be created at: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"Uploads will be stored in: {app.config['UPLOAD_FOLDER']}")
    app.run(debug=True)