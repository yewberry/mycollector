# -*- coding: utf-8 -*-
import os
import PyV8
import requests
import re
import json
import time
import urllib3
import base64
import pickle
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from my_glob import LOG

urllib3.disable_warnings()

class MyBaiduPan(object):

    def __init__(self, usr, pwd, ssl_verify=True):
        self.usr = usr
        self.pwd = pwd
        self.token = None
        self.gid = None
        self.dv = None
        self.PANPSC = None
        self.files = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
            "Accept-Encoding": "gzip, deflate, sdch"
        }
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.session.verify = ssl_verify
        self._initiate()

    def _initiate(self):
        if not self._load_cookies():
            LOG.debug("need login")
            _, self.dv, self.token = self._init_cookies()
            self.gid = self._gid()
            self._login()
            # get PANPSC in cookies
            self.session.get("http://pan.baidu.com/disk/home", params={
                "errno": "0",
                "errmsg": "Auth Login Sucess",
                "ssnerror": "0"
            })
            self._save_cookies()
        else:
            cks = self.session.cookies
            self.dv = cks.get("yew_dv")
            self.token = cks.get("yew_token")
            self.gid = self._gid()

    def listFiles(self):
        self.files.clear()
        self._list(cursor="null")
        return self.files

    def getUrlByPath(self, path):
        if path not in self.files:
            self.listFiles()
        f = self.files[path]
        if f is not None:
            fs_id = str(f["fs_id"])
            return self.getUrlById(fs_id)
        else:
            return []

    def getUrlById(self, fs_id):
        s = self.session
        sign, timestamp = self._sign()
        r = s.get("http://pan.baidu.com/api/download", params={
            "sign": sign,
            "timestamp": timestamp,
            "fidlist": "[{}]".format(fs_id),
            "type": "dlink",
            "channel": "chunlei",
            "web": "1",
            "app_id": "250528",
            "clienttype": "0",
        })
        o = json.loads(r.content)
        return o["dlink"]

    def _login(self):
        while True:
            payload = {
                "staticpage": "http://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html",
                "charset": "utf-8",
                "tpl": "netdisk",
                "subpro": "netdisk_web",
                "apiver": "v3",
                "codestring": "",
                "safeflg": "0",
                "u": "http://pan.baidu.com/disk/home",
                "isPhone": "false",
                "detect": "1",
                "quick_user": "0",
                "logintype": "basicLogin",
                "logLoginType": "pc_loginBasic",
                "idc": "",
                "loginmerge": "true",
                "foreignusername": "",
                "mem_pass": "on",
                "ppui_logintime": "7238",
                "countrycode": "",
                "fp_uid": "",
                "fp_info": "",
                "dv": self.dv,
                "username": self.usr,
                "password": self.pwd,
                "token": self.token,
                "tt": MyBaiduPan._timestamp(),
                "gid": self.gid,
            }
            r = self.session.post("https://passport.baidu.com/v2/api/?login", data=payload)
            # 需要输入验证码或验证码输入错误
            if "err_no=257" in r.content or "err_no=6" in r.content:
                code_string = re.findall(b'codeString=(.*?)&', r.content)[0]
                self.codeString = code_string
                LOG.debug('need captcha, codeString=' + code_string.decode('utf-8'))
# TODO
                continue
            break

    def _list(self, cursor):
        s = self.session
        r = s.get("http://pan.baidu.com/api/filediff", params={
            "cursor": cursor,
            "channel": "chunlei",
            "web": "1",
            "app_id": "250528",
            "clienttype": "0",
        }, cookies={
            "BDUSS": s.cookies.get("BDUSS"),
            "PANPSC": s.cookies.get("PANPSC")
        })
        o = json.loads(r.text)
        if o["errno"] == 0:
            l = o["entries"]
            has_more = o["has_more"]
            cursor = o["cursor"]
            for p in l:
                e = l[p]
                if e["isdir"] == 0:
                    self.files[e["path"]] = e
            if has_more:
                self._list(cursor)

    def _sign(self):
        """
        http://pan.baidu.com/disk/home?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0
        var context = {
        ...
        "sign2": "function s(j,r){var a=[];var p=[];var o=\"\";var v=j.length;for(var q=0;q<256;q++){a[q]=j.substr((q%v),1).charCodeAt(0);p[q]=q}for(var u=q=0;q<256;q++){u=(u+p[q]+a[q])%256;var t=p[q];p[q]=p[u];p[u]=t}for(var i=u=q=0;q<r.length;q++){i=(i+1)%256;u=(u+p[i])%256;var t=p[i];p[i]=p[u];p[u]=t;k=p[((p[i]+p[u])%256)];o+=String.fromCharCode(r.charCodeAt(q)^k)}return o};",
        ...
        }
        """
        def _sign2(j, r):
            a = []
            p = []
            o = ""
            v = len(j)
            for q in range(256):
                a.append(ord(j[q % v]))
                p.append(q)
            u = 0
            for q in range(256):
                u = (u + p[q] + a[q]) % 256
                t = p[q]
                p[q] = p[u]
                p[u] = t
            i = 0
            u = 0
            for q in range(len(r)):
                i = (i + 1) % 256
                u = (u + p[i]) % 256
                t = p[i]
                p[i] = p[u]
                p[u] = t
                k = p[((p[i] + p[u]) % 256)]
                o += chr(ord(r[q]) ^ k)
            return base64.b64encode(o)

        s = self.session
        r = s.get("http://pan.baidu.com/disk/home")
        html = r.content
        sign1 = re.search(r'"sign1":"([A-Za-z0-9]+)"', html).group(1)
        sign3 = re.search(r'"sign3":"([A-Za-z0-9]+)"', html).group(1)
        timestamp = re.search(r'"timestamp":([0-9]+)[^0-9]', html).group(1)
        sign = _sign2(sign3, sign1)
        return sign, timestamp

    def _token(self):
        r = self.session.get("https://passport.baidu.com/v2/api/?getapi", params={
            "tpl": "netdisk",
            "subpro": "netdisk_web",
            "apiver": "v3",
            "tt": MyBaiduPan._timestamp(),
            "class": "login",
            "gid": self.gid,
            "logintype": "basicLogin",
            "callback": "0"
        })
        o = json.loads(r.text.replace("\'", "\""))
        return o["data"]["token"]

    def _gid(self):
        # in login_tangram_xxxxxxx.js
        jsctx = PyV8.JSContext()
        jsctx.enter()
        _gid = jsctx.eval("""
            (function(){
                return "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,
                    function(e) {
                        var t = 16 * Math.random() | 0,
                        n = "x" == e ? t: 3 & t | 8;
                        return n.toString(16)
                    }).toUpperCase()
            })
        """)
        gid = _gid()
        jsctx.leave()
        return gid

    def _init_cookies(self):
        baiduid = None
        dv = None
        token = None
        while True:
            driver = webdriver.PhantomJS(executable_path="./phantomjs.exe")
            driver.get("http://pan.baidu.com")
            el = driver.find_element_by_id("pageSignupCtrl")
            act = ActionChains(driver)
            act.move_to_element(el).perform()
            el = driver.find_element_by_id("dv_Input")
            dv = el.get_attribute("value")
            baiduid = driver.get_cookie("BAIDUID")["value"]
            token = driver.execute_script("return window.$BAIDU$._maps_id['TANGRAM__PSP_4'].bdPsWtoken")
            driver.quit()
            cks = self.session.cookies
            cks.set("BAIDUID", baiduid)
            cks.set("yew_dv", dv)
            cks.set("yew_token", token)
            if (baiduid is not None) and (dv is not None) and (token is not None):
                break
            else:
                baiduid = None
                dv = None
                token = None

        LOG.debug("dv:{}\nBAIDUID:{}\ntoken:{}".format(dv, baiduid, token))
        return baiduid, dv, token

    def _callback(self):
        # in login_tangram_xxxxxxx.js
        jsctx = PyV8.JSContext()
        jsctx.enter()
        _cb = jsctx.eval("""
            (function(){
                return "bd__cbs__" + Math.floor(Math.random() * 2147483648).toString(36);
            })
        """)
        cb = _cb()
        jsctx.leave()
        return cb

    def _save_cookies(self):
        cookies_file = "{0}.cookies".format(self.usr)
        with open(cookies_file, "wb") as f:
            pickle.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

    def _load_cookies(self):
        cookies_file = "{0}.cookies".format(self.usr)
        LOG.debug("cookies file:" + cookies_file)
        if os.path.exists(cookies_file):
            LOG.debug("%s cookies file has already existed." % self.usr)
            with open(cookies_file, "rb") as cookies_file:
                cookies = requests.utils.cookiejar_from_dict(pickle.load(cookies_file))
                LOG.debug(str(cookies))
                self.session.cookies = cookies
                return True
        else:
            return False

    @staticmethod
    def _timestamp():
        return "%u" % (time.time()*1000)









