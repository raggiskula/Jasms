import urllib
import urllib2
import re
from suds.client import Client

def senda_sms(number, message):
    """docstring for senda_sms"""
    nova_soap = "http://www.nova.is/services/SupportService.asmx?wsdl"
    client = Client(nova_soap)
    result = client.service.sendSMS(number,message)
    if result.returnCode == 0:
        return

    URL = 'http://ja.is/sms/'
    o = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
    urllib2.install_opener(o)
    f = o.open(URL)
    content = f.read()
    max_sec = ''.join(re.search(r'"(\d+)" name="max25security', 
        content, re.MULTILINE).groups())    
    lines = content.split('\n')    
    js_index = [i for (i, l) in enumerate(lines) 
        if l.find('var scope =') > -1][0]

    d = dict([(k.strip().split()[1][0:-2], '%s: %s' % (
            k.strip().replace('function','def'), 
        v.strip()[0:-1])) for (k,v) in [
        func.strip()[0:-1].split('{') for func in 
            lines[js_index+1:js_index+5]]])
    
    for k,v in d.items():
        exec(v)        

    postval = locals().get(lines[js_index+8].strip().split()[-1][0:-3])() * -1
    params = {
        'sms_phone': number,
        'sms_message': message,
        'val': postval,
        'max25security': max_sec}        
    f = o.open(URL, urllib.urlencode(params))

if __name__ == "__main__":
    senda_sms("7775333", "hi")
