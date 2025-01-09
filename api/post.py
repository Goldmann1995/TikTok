import requests
import json

def post_bazi():
    url = "http://localhost:5000/bazi"
    headers = {"Content-Type": "application/json"}
    data = {
        "year": 1995,
        "month": 10, 
        "day": 29,
        "hour": 4,
        "name": "bagdsa",
        "gender": "female"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {e}")

if __name__ == "__main__":
    post_bazi()
