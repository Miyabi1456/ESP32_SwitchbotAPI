def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF) #ステーション用(ESP8266がルータに接続する場合)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('ssid', 'key') #ここに接続したいWiFiのSSIDとパスワードを書く
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig()) #IPアドレス、ネットマスク、ゲートウェイ、DNS
    
if __name__ == "__main__":
    do_connect()