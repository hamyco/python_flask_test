from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    name = request.args.get('name')
    return render_template('hello.html', title='flask test', name=name)

## おまじない
if __name__ == "__main__":
    app.run(debug=True)