import requests

MISSKEY_INSTANCE = "https://kmmi-skey.com/"  # 自分のMisskeyインスタンスのURL
API_TOKEN = "lARnsD6Q0BAwvIr0l3t90Ob6veMh561V"  # 発行したAPIトークン

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



