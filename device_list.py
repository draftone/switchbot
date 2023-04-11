import json
import time
import hashlib
import hmac
import base64
import requests
import uuid
import argparse
import os

base_url = 'https://api.switch-bot.com'

def make_sign(token: str, secret: str):
    nonce = ''
    t = int(round(time.time() * 1000))
    string_to_sign = bytes(f'{token}{t}{nonce}', 'utf-8')
    secret = bytes(secret, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign, str(t), nonce

def make_request_header(token: str, secret: str) -> dict:
    sign, t, nonce = make_sign(token, secret)
    headers = {
        "Authorization": token,
        "sign": sign,
        "t": str(t),
        "nonce": nonce
    }
    return headers

def read_token_secret(token_secret_file: str, service_name: str) -> tuple:
    with open(token_secret_file, mode='rt', encoding='utf-8') as f:
        data = json.load(f)
        service_data = data.get(service_name)
        token = service_data.get("token")
        secret = service_data.get("secret")
    return token, secret

def get_device_list(deviceListJson='deviceList.json', token_secret_file='token_secret.json', service_name='switch_bot'):
    token, secret = read_token_secret(token_secret_file, service_name)

    devices_url = base_url + "/v1.1/devices"

    headers = make_request_header(token, secret)

    try:
        # APIでデバイスの取得を試みる
        res = requests.get(devices_url, headers=headers)
        res.raise_for_status()

        print(res.text)
        deviceList = json.loads(res.text)
        # 取得データをjsonファイルに書き込み
        with open(deviceListJson, mode='wt', encoding='utf-8') as f:
            json.dump(deviceList, f, ensure_ascii=False, indent=2)

    except requests.exceptions.RequestException as e:
        print('response error:',e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--token_secret_file', type=str, default=os.path.expanduser(r'~\.key\token_secret.json'),
                        help='JSON file that stores service-specific API tokens and secrets')
    args = parser.parse_args()

    get_device_list(token_secret_file=args.token_secret_file)