import boto3
import uuid # ユニークなIDを生成するためにインポート
import datetime
from flask import Flask, request, redirect, url_for

# Flaskアプリケーションを作成
app = Flask(__name__)

# DynamoDBに接続
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Memos') #AWSで作成したテーブル名

memos = []

# ルートURL ("/") にアクセスがあったときの処理
@app.route("/")
def index():

    # DynamoDBから全件スキャンしてメモを取得
    response = table.scan()
    memos = response.get('Items',[])
    sorted_memos = sorted(memos, key=lambda x: x.get('created_at', ''), reverse=True)

    memo_list_html = ""
    # DynamoDBのデータは辞書形式なので、キーを指定して値を取り出す
    for memo in sorted_memos:
        display_time = memo.get('created_at', '日時不明')
        memo_list_html += f"<li>{memo['memo_text']} ({display_time}) <a href='/delete/{memo['memo_id']}'>削除</a></li>"

    form_html=f"""
   # この行を変更
    <h1>Simple Memo App (with DynamoDB) V2</h1>
    <form action="/add" method="post">
        <input type="text" name="memo" size="40" placeholder="メモを入力">
        <button type="submit">Add</button>
    </form>
    <h2>Memos:</h2>
    <ul>
        {memo_list_html}
    </ul>
    """
    return form_html

@app.route("/add", methods=["POST"])
def add_memo():

    memo_text = request.form["memo"]

    # ユニークなIDを生成
    memo_id = str(uuid.uuid4())

    created_at = datetime.datetime.now().isoformat()

    # DynamoDBにアイテムを書き込む
    table.put_item(
        Item = {
            'memo_id':memo_id,
            'memo_text':memo_text,
            'created_at': created_at
        }
    )

    return redirect(url_for("index"))

@app.route("/delete/<string:memo_id>")
def delete_memo(memo_id):

    table.delete_item(
        Key = {
            'memo_id':memo_id
        }
    )
    return redirect(url_for("index"))

# このファイルが直接実行された場合にサーバーを起動
if __name__ == "__main__":
    app.run(debug=True, port=5001)

