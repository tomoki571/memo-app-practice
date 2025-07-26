from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# メモを保存するためのリスト（簡易データベース）
memos = []

@app.route("/")
def index():
    # 保存されているメモを一覧表示するHTMLを生成
    memo_list_html = ""
    for memo in memos:
        memo_list_html += f"<li>{memo}</li>"

    # フォームとメモ一覧を組み合わせたHTML
    form_html = f"""
    <h1>Simple Memo App</h1>
    <form action="/add" method="post">
        <input type="text" name="memo" size="30" placeholder="メモを入力">
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
    # フォームから'memo'という名前のデータを取得
    memo_text = request.form["memo"]
    
    # リストにメモを追加
    memos.append(memo_text)
    
    # トップページにリダイレクト（移動）
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)