#app.py
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = 'kor-polimeter'

    from views import chart

    app.register_blueprint(chart, url_prefix = '/')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)