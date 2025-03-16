import requests
from bs4 import BeautifulSoup
import json
import os
import logging
from datetime import datetime
import google.cloud.logging
from google.cloud.logging import DESCENDING
from google.cloud import storage


#日付設定
exectuion_date = datetime.today().strftime("%Y-%m-%d")

#Cloud Loggingの初期化
client = google.cloud.logging.Client()
client.setup_logging()

def log_message(message):
    logging.info(f"{datetime.now()} - {message}")


def biteki_scraper():
    url = "https://www.biteki.com/"  # 取得したいWebサイトのURL
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        log_message(f"スクレイピング失敗（美的）：{e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("div.texts")  # 記事リンクを含む親要素を取得
    results = []

    for article in articles:
        link_tag = article.find("a")  # div 内の最初の <a> タグを取得
        if link_tag:
            title = article.find("h3").text if article.find("h3") else "タイトルなし"
            link = link_tag["href"]
            results.append({"title": title, "link": link,"date":exectuion_date})

    return results  # 記事のリストを返す



def scrape_and_save(request):
    articles = biteki_scraper()
    print("関数が実行されました")
    return f"美的の記事を処理しました。", 200

