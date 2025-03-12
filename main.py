from post_to_misskey import post_to_misskey # Misskey投稿関数をインポート
from datetime import datetime
import os
import json
from flask import Flask, request

app = Flask(__name__)

#ログファイル設定
LOG_FILE = "log.txt"

def log_message(message):
    with open(LOG_FILE,"a",encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n" )

#jsonファイル読み込み
JSON_FILE = "articles.json"

#JSONファイルを読み込む
def load_articles(filename):   
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

#JSONファイルを保存する
def save_articles(filename, articles):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

# 記事リストを読み込む
articles = load_articles(JSON_FILE)

# Misskeyに投稿
POST_COUNT = 2

def post_articles():
    articles = load_articles(JSON_FILE)

    if not articles:
        log_message("投稿する記事がありません。")
        return
    
    remaining_articles = []
    post_count = 0

    for article in articles:
        if post_count >= POST_COUNT:
            break #3件投稿したら終了

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

    save_articles(JSON_FILE,remaining_articles + articles[post_count:])
    log_message(f"{post_count}件の記事を投稿しました。")


if __name__ == "__main__":
    post_articles()

def beauty_bot_logic():
    result = post_articles()
    return "Beauty Bot is working!"

@app.route("/", methods=["GET", "POST"])
def handle_request():
    return beauty_bot_logic()

# Cloud Functions 用のエントリポイント
def beauty_bot_function(request):
    return beauty_bot_logic()
