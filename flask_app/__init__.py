from flask import Flask

app = Flask(__name__)


app.secret_key = "llave secretísima"

app.config['UPLOAD_FOLDER'] = 'flask_app/static/img'