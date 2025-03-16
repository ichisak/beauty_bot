from google.cloud import storage
import get_articles_voce
import get_articles_maquia
import get_articles_biteki
import requests

from flask import Flask,request
import json
import logging
from datetime import datetime
import google.cloud.logging

app = Flask(__name__)

#Cloud Loggingの初期化
client = google.cloud.logging.Client()
client.setup_logging()

#日付設定
exectuion_date = datetime.today().strftime("%Y-%m-%d")

def log_message(message):
    logging.info(f"{datetime.now()} - {message}")

def save_unique_results(results,filename="articles.json"):
    bucket_name = 'beauty-info-bot'
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    #バケット内のファイル取得
    blob = bucket.blob(filename)
    try:
        #既存のファイルがあれば読み込む
        existing_results = json.loads(blob.download_as_text())
    except Exception as e:
        log_message(f"ファイルの読み込みエラー: {e}")
        existing_results = []

    #すでに存在するデータをチェック
    existing_links = {item["link"] for item in existing_results}
    unique_results = [item for item in results if item["link"] not in existing_links]
    
    # 新しいデータがあれば追加
    if unique_results:
        existing_results.extend(unique_results)
        try:
            blob.upload_from_string(json.dumps(existing_results,ensure_ascii=False,indent=4))
            log_message(f"{len(unique_results)}件の新規記事を保存しました。（美的）")
        except Exception as e:
            log_message(f"データのアップロードエラー: {e}")
    else:
        log_message(f"新規記事はありませんでした。（美的）")
    return len(unique_results)  # 追加したデータ数を返す


@app.route("/", methods=["GET", "POST"])
def index():
    return scrape_and_save(request)

def scrape_and_save(request):
    try:
        print("Scraping started...")

        #各サイトのスクレイピングして保存
        biteki_articles = get_articles_biteki.biteki_scraper()
        print(f"biteki Articles fetched: {len(biteki_articles)}")
        save_unique_results(biteki_articles, filename="articles.json")
        
        
        voce_articles = get_articles_voce.voce_scraper()
        print(f"Voce Articles fetched: {len(voce_articles)}")
        save_unique_results(voce_articles, filename="articles.json")

        maquia_articles = get_articles_maquia.maquia_scraper()
        print(f"Maquia Articles fetched: {len(maquia_articles)}")
        save_unique_results(maquia_articles, filename="articles.json")



        print("関数が実行されました")
    except Exception as e:
        print(f"Error during scraping: {e}")
        return "Error during scraping", 500
    return 'Scraping done', 200

if __name__ == "__main__":
    app.run(debug=True)