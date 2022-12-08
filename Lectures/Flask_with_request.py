from flask import Flask
from flask import request


app = Flask(__name__)


@app.route('/')
def index():
    return 'Home Page'

@app.route('/career/')
def career():
    return 'Career Page'


@app.route('/contact/')
@app.route('/feedback/')
def feedback():
    return 'Feedback Page'

@app.route('/user/<id>/')
def user_profile(id):
    return "Profile page of user #{}".format(id)

@app.route('/find/user')
def find_user():
    user_name = request.args.get('name')
    return f"Searching for user by name '{user_name}'"


if __name__ == "__main__":
    app.run()