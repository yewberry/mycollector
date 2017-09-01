# -*- coding: utf-8 -*-
from functools import wraps
import os
import requests
import re
import json
import time
import urllib3
import base64
import pickle
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from my_glob import LOG
from ui_dlg_captcha import MyCaptchaDialog

try:
    urllib3.disable_warnings()
except:
    pass

REQUEST_TEMPLATE = {
    "headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
        "Accept-Encoding": "gzip, deflate, sdch",
    },
    "token": {
        "method": "get",
        "url": "https://passport.baidu.com/v2/api/?getapi",
        "params": {
            "tpl": "netdisk",
            "subpro": "netdisk_web",
            "apiver": "v3",
            "class": "login",
            "gid": None,
            "logintype": "basicLogin",
            "callback": "0"
        }
    },
    "login": {
        "method": "post",
        "url": "https://passport.baidu.com/v2/api/?login",
        "data": {
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
            "ppui_logintime": "7237",
            "countrycode": "",
            "dv": None,
            "username": None,
            "password": None,
            "token": None,
            "gid": None,
        }
    },
    "list": {
        "method": "get",
        "url": "http://pan.baidu.com/api/filediff",
        "params": {
            "cursor": None,
            "channel": "chunlei",
            "web": "1",
            "app_id": "250528",
            "clienttype": "0",
        }
    }
}

def check_login(func):
    """check user login status
    :param func: func to check
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        if type(ret) == requests.Response:
            try:
                foo = json.loads(ret.content.decode('utf-8'))
                if 'errno' in foo and foo['errno'] == -6:
                    LOG.debug('Offline, deleting cookies file then relogin.')
                    args[0]._remove_cookies()
                    args[0]._initiate()
            except:
                LOG.error('User unsigned in.')
        return ret
    return wrapper

class MyBaiduPan(object):

    def __init__(self, usr, pwd, ssl_verify=True):
        self.usr = usr
        self.pwd = pwd
        self.token = None
        self.gid = None
        self.dv = None
        self.files = {}
        self.session = None
        self.session = requests.Session()
        self.session.headers.update(REQUEST_TEMPLATE["headers"])
        self.session.verify = ssl_verify
        self._initiate()

    def _initiate(self):
        if not self._load_cookies():
            LOG.debug("Need login")
            self.session.get("http://www.baidu.com")
            self.gid = self._gid()
            self.token = self._token()
            self._login()
            # get PANPSC in cookies
            self.session.get("http://pan.baidu.com/disk/home", params={
                "errno": "0",
                "errmsg": "Auth Login Sucess",
                "ssnerror": "0"
            })
            # self._save_cookies()
        else:
            cks = self.session.cookies
            self.dv = cks.get("yew_dv")
            self.token = cks.get("yew_token")
            self.gid = self._gid()

    def _login(self):
        r = self._req("login", data={
            "dv": "",
            "username": self.usr,
            "password": self.pwd,
            "token": self.token,
            "gid": self.gid,
        }, params=None, cookies={})

        if "err_no=257" in r.content or "err_no=6" in r.content:
            code_string = re.findall(b'codeString=(.*?)&', r.content)[0]
            self.codeString = code_string
            LOG.debug('need captcha, codeString=' + code_string.decode('utf-8'))
            # captcha = self._get_captcha(code_string)
            dlg = MyCaptchaDialog(None, title="ABC", pth="mini_113.png")
            dlg.CenterOnScreen()
            dlg.ShowModal()

        # 需要输入验证码或验证码输入错误
        if "err_no=0" not in r.content:
            LOG.debug("Login fail")
            self._remove_cookies()

    def list_files(self):
        self.files.clear()
        self._list_files(cursor="null")
        return self.files

    def _list_files(self, cursor):
        r = self._request("list", params={"cursor": cursor})
        o = json.loads(r.content)
        if o["errno"] == 0:
            l = o["entries"]
            has_more = o["has_more"]
            cursor = o["cursor"]
            for p in l:
                e = l[p]
                if e["isdir"] == 0:
                    self.files[e["path"]] = e
            if has_more:
                self._list_files(cursor)

    def getUrlByPath(self, path):
        if path not in self.files:
            self.list_files()
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

    def _get_captcha(self, code_string):
        if code_string:
            u = "https://passport.baidu.com/cgi-bin/genimage?" + code_string.decode('utf-8')
            verify_code = self._captcha_func(u)
        else:
            verify_code = ""
        return verify_code

    def _captcha_func(self, url):
        return ""

    def _init_cookies(self):
        """
        method Oo and co in 6.min.js generate "dv" from mouse event. This only reason I use PhantomJS.
        I hope reimplement it in Python.

        metho _initApi in login_tangram.js initialize login "token" in window.$BAIDU$._maps_id['TANGRAM__PSP_4'].bdPsWtoken.
        :return: BAIDUID, dv, token

        """
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

        LOG.debug("dv:{}\nBAIDUID:{}\ntoken:{}".format(dv, baiduid, token))
        return baiduid, dv, token

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

    def _remove_cookies(self):
        cookies_file = "{0}.cookies".format(self.usr)
        if os.path.exists(cookies_file):
            os.remove(cookies_file)

    def _token(self):
        r = self._req("token", params={
            "tt": MyBaiduPan._timestamp(),
            "gid": self.gid,
        }, data=None, cookies={})
        o = json.loads(r.text.replace("\'", "\""))
        return o["data"]["token"]

    def _sign(self):
        s = self.session
        r = s.get("http://pan.baidu.com/disk/home")
        html = r.content
        sign1 = re.search(r'"sign1":"([A-Za-z0-9]+)"', html).group(1)
        sign3 = re.search(r'"sign3":"([A-Za-z0-9]+)"', html).group(1)
        timestamp = re.search(r'"timestamp":([0-9]+)[^0-9]', html).group(1)
        sign = MyBaiduPan._sign2(sign3, sign1)
        return sign, timestamp

    @check_login
    def _request(self, req_id=None, params=None, data=None, cookies=None):
        params = {} if params is None else params
        data = {} if data is None else data
        cookies = {} if cookies is None else cookies
        if req_id not in REQUEST_TEMPLATE:
            LOG.error("Request cfg of %s not found" % req_id)
            return None
        return self._req(req_id, params, data, cookies)

    def _req(self, req_id, params, data, cookies):
        s = self.session
        req_cfg = REQUEST_TEMPLATE[req_id]
        m = req_cfg["method"]
        u = req_cfg["url"]
        s.cookies.update(cookies)
        if m == "get":
            p = req_cfg["params"].copy()
            p.update({"tt": MyBaiduPan._timestamp()})
            p.update(params)
            resp = s.get(u, params=p)
        else:
            d = req_cfg["data"].copy()
            d.update({"tt": MyBaiduPan._timestamp()})
            d.update(data)
            resp = s.post(u, data=d)
        return resp

    @staticmethod
    def _sign2(j, r):
        """
        http://pan.baidu.com/disk/home?errno=0&errmsg=Auth%20Login%20Sucess&&bduss=&ssnerror=0
        var context = {
        ...
        "sign2": "function s(j,r){var a=[];var p=[];var o=\"\";var v=j.length;for(var q=0;q<256;q++){a[q]=j.substr((q%v),1).charCodeAt(0);p[q]=q}for(var u=q=0;q<256;q++){u=(u+p[q]+a[q])%256;var t=p[q];p[q]=p[u];p[u]=t}for(var i=u=q=0;q<r.length;q++){i=(i+1)%256;u=(u+p[i])%256;var t=p[i];p[i]=p[u];p[u]=t;k=p[((p[i]+p[u])%256)];o+=String.fromCharCode(r.charCodeAt(q)^k)}return o};",
        ...
        }
        """
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

    @staticmethod
    def _gid():
        r = ""

        def a(e):
            t = int(16 * random.random())
            n = t if "x" == e else 3 & t | 8
            return ("%x" % n).upper()
        for c in "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx":
            if c in "xy":
                r += a(c)
            else:
                r += c
        return r

    @staticmethod
    def _timestamp():
        return "%u" % (time.time()*1000)

    ###########################################################################
    # NOT USED
    ###########################################################################
    # def _token(self):
    #     r = self.session.get("https://passport.baidu.com/v2/api/?getapi", params={
    #         "tpl": "netdisk",
    #         "subpro": "netdisk_web",
    #         "apiver": "v3",
    #         "tt": MyBaiduPan._timestamp(),
    #         "class": "login",
    #         "gid": self.gid,
    #         "logintype": "basicLogin",
    #         "callback": "0"
    #     })
    #     o = json.loads(r.text.replace("\'", "\""))
    #     return o["data"]["token"]

    # def _callback(self):
    #     # in login_tangram_xxxxxxx.js
    #     jsctx = PyV8.JSContext()
    #     jsctx.enter()
    #     _cb = jsctx.eval("""
    #         (function(){
    #             return "bd__cbs__" + Math.floor(Math.random() * 2147483648).toString(36);
    #         })
    #     """)
    #     cb = _cb()
    #     jsctx.leave()
    #     return cb

    # def _gid(self):
    #     # in login_tangram_xxxxxxx.js
    #     jsctx = PyV8.JSContext()
    #     jsctx.enter()
    #     _gid = jsctx.eval("""
    #         (function(){
    #             return "xxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g,
    #                 function(e) {
    #                     var t = 16 * Math.random() | 0,
    #                     n = "x" == e ? t: 3 & t | 8;
    #                     return n.toString(16)
    #                 }).toUpperCase()
    #         })
    #     """)
    #     gid = _gid()
    #     jsctx.leave()
    #     return gid

    # def _init_cookies(self):
    #     """
    #     method Oo and co in 6.min.js generate "dv" from mouse event. This only reason I use PhantomJS.
    #     I hope reimplement it in Python.
    #
    #     metho _initApi in login_tangram.js initialize login "token" in window.$BAIDU$._maps_id['TANGRAM__PSP_4'].bdPsWtoken.
    #     :return: BAIDUID, dv, token
    #
    #     """
    #     while True:
    #         driver = webdriver.PhantomJS(executable_path="./phantomjs.exe")
    #         driver.get("http://pan.baidu.com")
    #         el = driver.find_element_by_id("pageSignupCtrl")
    #         act = ActionChains(driver)
    #         act.move_to_element(el).perform()
    #         el = driver.find_element_by_id("dv_Input")
    #         dv = el.get_attribute("value")
    #         baiduid = driver.get_cookie("BAIDUID")["value"]
    #         token = driver.execute_script("return window.$BAIDU$._maps_id['TANGRAM__PSP_4'].bdPsWtoken")
    #         driver.quit()
    #         cks = self.session.cookies
    #         cks.set("BAIDUID", baiduid)
    #         cks.set("yew_dv", dv)
    #         cks.set("yew_token", token)
    #         if (baiduid is not None) and (dv is not None) and (token is not None):
    #             break
    #
    #     LOG.debug("dv:{}\nBAIDUID:{}\ntoken:{}".format(dv, baiduid, token))
    #     return baiduid, dv, token




