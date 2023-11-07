from flask import Flask, render_template
from flasgger import Swagger

from main.controller.user_controller import user


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024
app.register_blueprint(user, url_prefix="/user")
Swagger(app)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=true)
