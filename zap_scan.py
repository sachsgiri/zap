# -*- coding: utf-8 -*-
import time
from pprint import pprint
from zapv2 import ZAPv2
import urllib

# Here the target is defined and an instance of ZAP is created.
target = 'https://10.11.15.176/login'
apikey = 'apiji'
#zap = ZAPv2()

# Use the line below if ZAP is not listening on 8090.
zap = ZAPv2(proxies={'http': 'http://172.17.0.2:8090', 'https': 'http://172.17.0.2:8090'}, apikey=apikey)

# ZAP starts accessing the target.
print('Accessing target %s' % target)
print(zap.urlopen(target))
time.sleep(4)

# The spider starts crawling the website for URL’s
print('Spidering target %s' % target)
zap.spider.scan(target, apikey=apikey)

# Progress of spider
time.sleep(2)
print('Status %s' % zap.spider.status())
while (int(zap.spider.status()) < 100):
   print('Spider progress %: ' + zap.spider.status())

   time.sleep(40)

print('Spider completed')

# Give the passive scanner a chance to finish
time.sleep(5)

# The active scanning starts
print('Scanning target %s' % target)
zap.ascan.scan(target, apikey=apikey)
while (int(zap.ascan.status()) < 100):
   print('Scan progress %: ' + zap.ascan.status())
   time.sleep(10)

print('Scan completed')

# Report the results
print('Hosts: ' + ', '.join(zap.core.hosts))
print('Alerts: ')
pprint(zap.core.alerts())


context_name = "auth_context"
context_id = zap.context.new_context(context_name, apikey=apikey)

print("context {} with id {}".format(context_name, context_id))

login_config_params = ''.join(("loginUrl=https://10.11.15.176/login/loginRequestData=",
                               urllib.quote_plus("{\"username\":\"userji\",\"password\":\"passji\"}")))

zap.authentication.set_authentication_method(context_id, "jsonBasedAuthentication",)