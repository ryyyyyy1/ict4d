from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route('/search', methods=['POST', 'GET'])
def search():
    print('searching...')
    if request.method == "GET":
        print(request)
        cert_id = request.args.get('cert_id')
        print(cert_id)
    else:
        print('unhandled method')
    return redirect(url_for('search_result'))


@app.route('/search_result')
def search_result():
    # 渲染搜索结果页面
    return render_template('certification.html')


@app.route("/test")
def test():
    return "this is a test"


if __name__ == '__main__':
    app.run()
