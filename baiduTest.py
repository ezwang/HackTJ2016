import requests as r
import os
import base64
import simplejson as js


def main():
    decoder = js.JSONDecoder()
    size = os.path.getsize('helloout.wav')
    speech = base64.b64encode(open('helloout.wav').read())
    print(type(speech))
    # token = r.post('https://openapi.baidu.com/oauth/2.0/token', data={'grant_type': 'client_credentials', 'client_id': 'Ib9tEFSgkT8ZdE3E9y0mBu6S', 'client_secret': '6e6d4d73cf5a3621f85793189d5e5382'})
    # print(token)
    # print(decoder.decode(token.content))
    out = r.post('http://vop.baidu.com/server_api', data={'format': 'wav', 'rate': 16000, 'cuid': '3c:97:0e:a3:bd:0a', 'channel': 1, 'token': '24.ed4c94f246a2fc77b2dfe5d9be077adc.2592000.1457411088.282335-7744184', 'speech': speech, 'len': len(speech)})
    print(out)
    print(decoder.decode(out.content))

if __name__ == '__main__':
    main()
