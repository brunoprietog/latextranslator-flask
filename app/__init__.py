from flask import Flask
from app.controllers.main_controller import translation

def create_app():
    app = Flask(__name__, static_folder='assets', template_folder='views')
    app.config['SECRET_KEY'] = '7110c8ae51a4b5af97be6534caef90e4bb9bdcb3380af008f90b23a5d1616bf319bc298105da20fe' 
    app.register_blueprint(translation, url_prefix='/')

    return app