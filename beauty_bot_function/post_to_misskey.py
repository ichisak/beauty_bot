import requests
from dotenv import load_dotenv
import os
import logging
import google.cloud.logging
from datetime import datetime

#Cloud Loggingの初期化
client = google.cloud.logging.Client()
client.setup_logging()
logging.basicConfig(level=logging.INFO)

#日付設定
exectuion_date = datetime.today().strftime("%Y-%m-%d")

#Loggingへログの書き込み
def log_message(message):
    logging.info(f"{datetime.now()} - {message}")


load_dotenv()

MISSKEY_INSTANCE = os.getenv("MISSKEY_URL")  # 自分のMisskeyインスタンスのURL
API_TOKEN = os.getenv("API_TOKEN") # 発行したAPIトークン

def post_to_misskey(text):
    url = f"{MISSKEY_INSTANCE}/api/notes/create"
    payload = {
        "i": API_TOKEN,
        "visibility": "home",
        "text": text
    }

    try:
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload,headers=headers)

        response.raise_for_status()
        
        if response.status_code == 200:
            data = response.json()
            if "createdNote" in data:
                return True
            else:
                log_message(f"投稿失敗（レスポンス異常）：{data}")
                return False
        else:
            log_message(f"投稿失敗（ステータスコード: {response.status_code}）：{response.text}")
            return False
    except requests.exceptions.RequestException as e:
        log_message(f"Misskey投稿エラー：{e}")
        return False



