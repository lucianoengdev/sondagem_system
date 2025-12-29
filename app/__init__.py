from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'b87274d4eab3636e09daf743e645fd57'
    app.config['UPLOAD_FOLDER'] = 'uploads'
    
    from . import routes
    app.register_blueprint(routes.bp)
    
    return app