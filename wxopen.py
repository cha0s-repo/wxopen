from flask import Flask, request
from wxapi.wxapi import WxApi
import hashlib
import logging

log_path = '/home/ubuntu/wxopen/log/run.log'
log_level = logging.DEBUG
logging.basicConfig(filename=log_path, level=log_level)

wx_uri = '/wxapi'

app = Flask(__name__)

wx = WxApi(log_path, log_level)

@app.route(wx_uri, methods=["GET"])
def server_get():
    if request.args is None:
        logging.debug('Get args none')
        return 'erro'
    else:
        return wx.cert_server(request.args.to_dict())

@app.route(wx_uri, methods=["POST"])
def server_post():
    if request.form is None:
        logging.error('Post form none')
        return 'error'
    else:
        logging.debug('data :' + request.data.decode('utf-8'))
        wx.cert_server(request.args.to_dict())
        return wx.post_server(request.data.decode('utf-8'))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
