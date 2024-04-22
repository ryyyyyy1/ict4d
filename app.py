from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "hello ict4d!"

@app.route("/test")
def test():
    return "this is a test"

if __name__ == '__main__':
    app.run()