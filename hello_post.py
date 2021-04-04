from flask import Flask, render_template, request #追加

app = Flask(__name__)

@app.route('/hello', methods=['POST']) #Methodを明示する必要あり
def hello_post():
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = "no name."
    return render_template('hello.html', title='flask test', name=name)

@app.route('/')
def hello_home():
    name = "Hoge"
    #return name
    return render_template('pre_hello.html', title='flask test', name=name) #変更

## おまじない
if __name__ == "__main__":
    app.run(debug=True)