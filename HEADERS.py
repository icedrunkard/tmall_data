# -*- coding: utf-8 -*-

headers={
'Host':'only.tmall.com',
'Connection':'keep-alive',
'Accept':'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
'DNT':'1',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4',
}

#代理服务器，每个请求换一个ip，地址https://www.abuyun.com
proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"

#代理隧道验证信息，购买后变更
proxyUser = "****************"
proxyPass = "****************"

proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

proxies = {
        "http"  : proxyMeta,
        "https" : proxyMeta,
    }
