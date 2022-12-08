from flask import Flask


app = Flask(__name__)



def index():
    return 'Hello World'

app.add_url_rule('/', 'index', index)


if __name__ == "__main__":
    app.run()
