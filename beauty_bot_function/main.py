import os
import json
from google.cloud import storage
import logging
import google.cloud.logging
from google.cloud.logging import DESCENDING
from datetime import datetime
from flask import Flask, request
from post_to_misskey import post_to_misskey # Misskey投稿関数をインポート

app = Flask(__name__)

#Cloud Loggingの初期化
client = google.cloud.logging.Client()
client.setup_logging()
logging.basicConfig(level=logging.INFO)
logging.info("ログ開始")

#日付設定
exectuion_date = datetime.today().strftime("%Y-%m-%d")

#Loggingへログの書き込み
def log_message(message):
    logging.info(f"{datetime.now()} - {message}")

#GCSの設定
BUCKET_NAME = "beauty-info-bot"
JSON_FILE = "articles.json"
LOCAL_JSON_FILE ="/tmp/articles.json"

#GCSから記事データをダウンロード
def load_articles(filename):
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(JSON_FILE)

    if not blob.exists():
        log_message("GCSに記事ファイルがありません。")
        return []
    
    #一時的にローカルにダウンロード
    blob.download_to_filename(LOCAL_JSON_FILE)

    #Json読み込み
    with open(LOCAL_JSON_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            log_message("JSONデコードエラー")
            return []


#JSONファイルをtmpに保存する
def save_articles(articles):
    # GCSにアップロード
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(JSON_FILE)

    try:    
        blob.upload_from_string(json.dumps(articles, ensure_ascii=False, indent=4))
        log_message(f"GCSにファイルをアップロードしました: {JSON_FILE}")
    except Exception as e:
        log_message(f"GCSアップロードエラー: {e}")


# Misskeyに投稿
POST_COUNT = 2

def post_articles():
    articles = load_articles(JSON_FILE)

    if not articles:
        log_message("投稿する記事がありません。")
        return
    
    remaining_articles = []
    post_count = 0

    for article in articles[:POST_COUNT]:
        title = article["title"]
        link = article["link"]
        text = f"📰 {title}\n🔗 {link}"
            
        response = post_to_misskey(text)

        if response:
            post_count += 1 #投稿したらカウントを増やす
            log_message(f"投稿成功: {title}")
        else:
            remaining_articles.append(article) #投稿に失敗した記事は残す
            log_message(f"投稿失敗: {title}")

    # 投稿に成功した記事は削除する
    remaining_articles.extend(articles[POST_COUNT:])
    save_articles(remaining_articles)
    log_message(f"{post_count}件の記事を投稿しました。")


@app.route("/", methods=["GET", "POST"])
def index():
    return beauty_bot_function(request)

# Cloud Functions 用のエントリポイント
def beauty_bot_function(request):
    log_message("Beauty Bot function started.")  # ログを追加
    try:
        post_articles()
    except Exception as e:
        logging.error(f"エラーが発生しました: {e}")
    return "Beauty Bot is working!"

if __name__ == "__main__":
    app.run(debug=True)