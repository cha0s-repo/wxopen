import logging
import hashlib
import xml.etree.ElementTree as xmlp
from time import time
from dicttoxml import dicttoxml

class WxApi:
    def __init__(self, log_path, log_level):
        logging.basicConfig(filename=log_path, level=log_level)

    def cert_server(self, req_msg):
        # req_msg should be dict
        if req_msg is None:
            logging.debug('Get args none')
            return 'erro'
        else:
            logging.debug(str(req_msg))
            sig = req_msg.get('signature')
            ts = req_msg.get('timestamp')
            nonce = req_msg.get('nonce')
            echostr = req_msg.get('echostr')

            token = 'gonorth2020'
            logging.debug(sig + '|' + ts + '|' + nonce)
            lst = [token, ts, nonce]
            slst = sorted(lst)
            cbstring = slst[0] + slst[1] + slst[2]

            if hashlib.sha1(cbstring.encode('utf-8')).hexdigest() == sig:
                logging.debug('certi ok')
                return echostr
            else:
                logging.error('certi failed')
                return 'error'
    def post_server(self, xml_msg):
        logging.debug('post msg: ' + xml_msg)
        in_msg = self.parse_xml(xml_msg)

        if in_msg['Content'] is not None:
            # process cmd
            return self.generate_msg(in_msg, 'test')
        else:
            # return default error msg
            logging.error('not get vaild msg')
            return 'error'

    def generate_msg(self, msg_fmt, msg):
        out_fmt = {}
        if msg_fmt['FromUserName'] is not  None:
            out_fmt['ToUserName'] = msg_fmt['FromUserName']
        else:
            logging.error('FromUserName is null')
            return None
        if msg_fmt['ToUserName'] is not None:
            out_fmt['FromUserName'] = msg_fmt['ToUserName']
        else:
            logging.error('ToUserName is null')
            return None
        out_fmt['CreateTime'] = str(int(time())) 
        out_fmt['MsgType'] = 'text'
        out_fmt['Content'] = msg

        res_xml = self.gen_xml(out_fmt)
        logging.debug('return msg: ' + res_xml)
        return res_xml

    def gen_xml(self, d_fmt):
        fmt_msg = '<xml><ToUserName><![CDATA[toholder]]></ToUserName><FromUserName><![CDATA[fromholder]]></FromUserName><CreateTime>timeholder</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[msgholder]]></Content></xml>'
        fmt_msg = fmt_msg.replace('toholder', d_fmt['ToUserName'])
        fmt_msg = fmt_msg.replace('fromholder', d_fmt['FromUserName'])
        fmt_msg = fmt_msg.replace('timeholder', d_fmt['CreateTime'])
        fmt_msg = fmt_msg.replace('msgholder', d_fmt['Content'])

        return fmt_msg


    def parse_xml(self, xml_str):
        res_dict = {}
        try:
            root = xmlp.fromstring(xml_str)
            for cc in root:
                logging.debug(cc.tag )
            res_dict['ToUserName'] = root.find('ToUserName').text
            res_dict['FromUserName'] = root.find('FromUserName').text
            res_dict['MsgType'] = root.find('MsgType').text
            res_dict['Content'] = root.find('Content').text
        except:
            logging.error('parse xml faild: ' + xml_str)
        return res_dict


