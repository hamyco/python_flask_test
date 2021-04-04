from flask import Flask, render_template, request, jsonify #追加

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False #ソートをそのまま

@app.route('/hello')
def hello():
    data = [
        {"name":"海敏さん"},
        {"age":12}
    ]
    return jsonify({
        'status':'OK',
        'data':data
    })

## おまじない
if __name__ == "__main__":
    app.run(debug=True)