"""
WEEK1：第一次模型呼叫

AI 協作紀錄：AI 協助整理程式架構；學生要自己閱讀程式，
並理解 API key 是從環境變數讀取，不能寫在這個檔案裡。

執行前先安裝 requests：
  py -m pip install requests

PowerShell 設定 API key（把右邊換成自己的 key；不要貼進作業或 GitHub）：
  $env:NVIDIA_API_KEY = "你的 NVIDIA API key"

執行：
  py week1_single_call.py
"""

import json
import os

import requests

API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
MODEL = "minimaxai/minimax-m3.1-flash"


def call_model(messages):
    # key 放在環境變數，不放進程式碼。
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        print("找不到 NVIDIA_API_KEY，請先在 PowerShell 設定環境變數。")
        return None

    # 這裡只送出一次 POST，請模型回答問題。
    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": messages,
                "max_tokens": 512,
                "temperature": 1,
                "top_p": 0.95,
            },
            timeout=60,
        )
    except requests.exceptions.RequestException as error:
        print("連線失敗：", error)
        return None

    print("status:", response.status_code)

    try:
        data = response.json()
    except ValueError:
        print("Response 不是 JSON：")
        print(response.text)
        return None

    # 印出完整 Response Body，方便和 curl -v 的結果對照。
    print(json.dumps(data, ensure_ascii=False, indent=2))

    if response.ok:
        # 模型回覆文字在 choices[0].message.content。
        reply = data["choices"][0]["message"]["content"]
        print("reply:", reply)
    else:
        # 失敗時先看 Status Code，再看服務回傳的 error。
        print("error:", data.get("error", data))

    return data


if __name__ == "__main__":
    question = "用一句話說明什麼是 HTTP"
    messages = [{"role": "user", "content": question}]
    call_model(messages)

