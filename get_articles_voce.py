from bs4 import BeautifulSoup
import requests
import re  # 正規表現モジュール
import json
import os
from datetime import datetime

#ログファイル設定
LOG_FILE = "log.txt"

def log_message(message):
    with open(LOG_FILE,"a",encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n" )

exectuion_date = datetime.today().strftime("%Y-%m-%d")

def voce_scraper():
    url = "https://i-voce.jp/feed/"  # 取得したいWebサイトのURL
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        log_message(f"スクレイピング失敗（美的）：{e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")    
    # /feed/を含むものを取得する  
    articles = soup.find_all("a", href=lambda href: href and href.startswith("/feed/"))
    results = []


    pattern = re.compile(r"/feed/\d{7}/$") # /feed/の後に7桁の数字
 
    for article in articles[:20]:
        link = article["href"]  #記事のリンクを取得
        
        #パターンマッチしたリンクとタイトルを保存
        if pattern.match(link):
            title_tag = article.find("div",class_="lineClamp title_Mn6uZ")
            if title_tag:
                title = title_tag.get_text(strip=True)  #テキストを取得
            link = article["href"]  # 記事のリンクを取得

            results.append({"title": title, "link": f"https://i-voce.jp{link}" , "date":exectuion_date})  

    return results

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
            log_message(f"{len(unique_results)}件の新規記事を保存しました。（VoCE）")
    else:
        log_message(f"新規記事はありませんでした。（VoCE）")

    return len(unique_results)  # 追加したデータ数を返す


# 実行して結果を表示
if __name__ == "__main__":
    articles = voce_scraper()
    save_unique_results(articles)

