import time
import hashlib
import hmac
import base64
import urequests

import network_connection
network_connection.do_connect()

# open token
token = '' # copy and paste from the SwitchBot app V6.14 or later
# secret key
secret = '' # copy and paste from the SwitchBot app V6.14 or later

def get_auth_header(token, secret):
    nonce = '' #空欄のままで良いらしい
    t = int(round((time.time() + 946684800) * 1000)) #UNIXとESP32のエポック基準時刻を合わせるために+946684800
    string_to_sign = '{}{}{}'.format(token, t, nonce)

    string_to_sign = bytes(string_to_sign, 'utf-8')
    secret = bytes(secret, 'utf-8')

    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, 
    digestmod=hashlib.sha256).digest())
    print ('Authorization: {}'.format(token))
    print ('t: {}'.format(t))
    print ('sign: {}'.format(str(sign, 'utf-8')))
    print ('nonce: {}'.format(nonce))

    header={}
    header["Authorization"] = token
    header["sign"] = str(sign, 'utf-8')
    header["t"] = str(t)
    header["nonce"] = nonce
    return header

host_domain = "https://api.switch-bot.com"
ver = "/v1.1"

def get_device_list(header):
    response = urequests.get(host_domain + ver + "/devices", headers=header)
    return_json = response.json()
    if return_json["message"] == "success":
        print("取得成功")
        return return_json["body"]
    elif return_json["message"] == "Unauthorized":
        print("認証エラー")
        return None
    else:
        print("エラー")
        return None
    
def get_th(header):
    th_deviceid = "" #デバイスIDを入力する
    response = urequests.get(host_domain + ver +"/devices/" + th_deviceid + "/status", headers=header)
    temperature = response.json()["body"]["temperature"]
    humidity = response.json()["body"]["humidity"]
    return temperature, humidity

if __name__ == "__main__":
    header = get_auth_header(token, secret)
    device_list = get_device_list(header)
    print(device_list)
    temperature, humidity = get_th(header)
    print(f"室温:{temperature}℃  湿度{humidity}%")
