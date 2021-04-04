from flask import Flask, render_template, jsonify #追加
import pymysql #追加

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False #日本語文字化け対策
app.config["JSON_SORT_KEYS"] = False #ソートをそのまま

def getConnection():
    return pymysql.connect(
        host='localhost',
        user='root',
        #password='root',
        db='haimin_testdb',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
    )

@app.route('/')
def hello():
    db = getConnection()
    cur = db.cursor()
    sql = "select * from members"
    cur.execute(sql)
    members = cur.fetchall()
    cur.close()
    db.close()

    return jsonify({
        'status':'OK',
        'members':members
    })

## おまじない
if __name__ == "__main__":
    app.run(debug=True)