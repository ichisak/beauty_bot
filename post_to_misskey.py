import requests
from dotenv import load_dotenv
import os

load_dotenv()

MISSKEY_INSTANCE = os.getenv("MISSKY_URL")  # 自分のMisskeyインスタンスのURL
API_TOKEN = os.getenv("API_TOKEN") # 発行したAPIトークン

def post_to_misskey(text):
    url = f"{MISSKEY_INSTANCE}api/notes/create"
    payload = {
        "i": API_TOKEN,
        "visibility": "home",
        "text": text
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()

        data = response.json()
        if "createdNote" in data:
            return True
        else:
            print(f"投稿失敗（レスポンス異常）：{data}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Misskey投稿エラー：{e}")
        return False



