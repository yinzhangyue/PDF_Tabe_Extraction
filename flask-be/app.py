from flask import Flask
from routes.auth import auth_bp
from routes.model import model_bp
from routes.pdf import pdf_bp
from conf.config import DevelopmentConfig


app = Flask(__name__)
app.register_blueprint(auth_bp)
app.register_blueprint(model_bp)
app.register_blueprint(pdf_bp)


if __name__ == '__main__':
    # config = DevelopmentConfig()
    # app.config.from_object('conf.config.DevelopmentConfig')
    # app.config.from_pyfile('conf/debugConfig.py')
    app.run(host='0.0.0.0')
