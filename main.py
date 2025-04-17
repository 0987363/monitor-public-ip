import requests
import time
import os
import argparse
from dotenv import load_dotenv

def get_public_ip():
    os.environ['NO_PROXY'] = 'checkip.amazonaws.com'
    try:
        response = requests.get("https://checkip.amazonaws.com", timeout=5, proxies={})
        response.raise_for_status()
        return response.text.strip()
    except requests.exceptions.RequestException as e:
        print(f"Query public IP failed: {e}")
        return None

def load_cached_ip(cache_file):
    try:
        with open(cache_file, "r") as f:
            return f.readline().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Load cache IP failed: {e}")
        return None

def save_cached_ip(cache_file, ip_address):
    try:
        with open(cache_file, "w") as f:
            f.write(ip_address + "\n")
    except Exception as e:
        print(f"Save cache IP failed: {e}")

def send_telegram_message(bot_token, chat_id, message):
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    params = {"chat_id": chat_id, "text": message}
    try:
        response = requests.post(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            print(f"Send Telegram message failed: {data.get('description')}")
    except requests.exceptions.RequestException as e:
        print(f"Send Telegram message failed: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--name", default="My", help="network name")
    parser.add_argument("--cache", default="./public_ip_cache.txt", help="cache file path")
    parser.add_argument("--token", help="Telegram bot token.")
    parser.add_argument("--chat", help="Telegram chat id.")

    args = parser.parse_args()

    if not args.token or not args.chat:
        print("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID please.")
        exit(1)

    last_ip = load_cached_ip(args.cache)
    print(f"Last IP: {last_ip}")

    current_ip = get_public_ip()

    if current_ip:
        print(f"Current IP: {current_ip}")
        if current_ip != last_ip:
            message = f"{args.name} Public IP modified！\nOld IP: {last_ip}\nNew IP: {current_ip}"
            send_telegram_message(args.token, args.chat, message)
            save_cached_ip(args.cache, current_ip)
        else:
            print("IP no change.")
    else:
        print("Could not query current public IP, ignore check.")

