import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

#日付設定
exectuion_date = datetime.today().strftime("%Y-%m-%d")

#ログファイル設定
LOG_FILE = "log.txt"

def log_message(message):
    with open(LOG_FILE,"a",encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n" )


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


def save_unique_results(results,filename="articles.json"):
    if os.path.exists(filename):
         with open(filename,"r",encoding="utf-8") as f:
            try:
                existing_results = json.load(f)
            except json.JSONDecodeError:
                existing_results = []
    else:
            existing_results = []

    #すでに存在するデータをチェック
    existing_links = {item["link"] for item in existing_results}
    unique_results = [item for item in results if item["link"] not in existing_links]

    # 新しいデータがあれば追加
    if unique_results:
        existing_results.extend(unique_results)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(existing_results, f, ensure_ascii=False, indent=4)
            log_message(f"{len(unique_results)}件の新規記事を保存しました。（美的）")
    else:
        log_message(f"新規記事はありませんでした。（美的）")
    return len(unique_results)  # 追加したデータ数を返す


# 関数を呼び出して出力
if __name__ == "__main__":
    articles = biteki_scraper()
    save_unique_results(articles)
