import os
import subprocess
from dotenv import load_dotenv
from openai import AzureOpenAI

def main():
    load_dotenv()
    endpoint = os.environ.get("AZURE_AI_ENDPOINT")
    api_key = os.environ.get("AZURE_AI_KEY")
    deployment = os.environ.get("AZURE_AI_DEPLOYMENT", "gpt-4o-mini")
    api_version = os.environ.get("AZURE_AI_API_VERSION", "2024-12-01-preview")

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=api_key,
    )

    user_input = input("請輸入你想讓本地端執行的任務：")
    system_prompt = (
        "你是一個 macOS agent，請根據使用者輸入，產生一條可以在 macOS 終端機執行的指令。"
        "如果是開啟網站，請用 'open -a Safari <網址>' 格式。只輸出指令，不要有多餘說明。"
    )
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input},
        ],
        max_tokens=256,
        temperature=0,
        top_p=1.0,
        model=deployment
    )
    command = response.choices[0].message.content.strip()
    print(f"執行指令：{command}")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"指令執行失敗：{e}")

if __name__ == "__main__":
    main()
