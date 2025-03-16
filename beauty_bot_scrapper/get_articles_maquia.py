import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

exectuion_date = datetime.today().strftime("%Y-%m-%d")

#ログファイル設定
LOG_FILE = "log.txt"

def log_message(message):
    with open(LOG_FILE,"a",encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n" )


def maquia_scraper():
    url = "https://maquia.hpplus.jp/topics/"  # 取得したいWebサイトのURL
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        log_message(f"スクレイピング失敗（美的）：{e}")
        return []
    
    soup = BeautifulSoup(response.text, "html.parser")
    #親要素を取得
    articles = soup.select_one("div.main-top")
    results = []

    if articles:
        article_cards = articles.find_all("div",class_="article-card-body")
        for article in article_cards:
            link_tag = article.find("a",href=True)
            title_tag = article.find("h3")
            
            if link_tag and title_tag:
                title = title_tag.get_text(strip=True)
                link = link_tag["href"]
                results.append({"title": title, "link": link,"date":exectuion_date})

    return results  # 記事のリストを返す


# 関数を呼び出して出力
if __name__ == "__main__":
    articles = maquia_scraper()
