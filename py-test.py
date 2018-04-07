#!/usr/bin/python3
import requests, pickle
import RSAEncode
import json
import os

COOKIE_FILE = './cookies'
CONFIG_FILE = './config.json'
REQUEST_INFO_FILE = './testInfo.json'

def loadJsonFromFile(filePath):
    with open(filePath, 'r') as f:
        loadDict = json.load(f)
        return loadDict

config = loadJsonFromFile(CONFIG_FILE)
HOST = config['host']
ENCODE_MSG_URL = config['encryptMsgUrl']
LOGIN_URL = config['loginUrl']
USER_NAME = config['userName']
PWD = config['pwd']

def getEncryptMsg():
    r = requestUrl(ENCODE_MSG_URL, {})
    return json.loads(r.text)

def getEncodePwd(pwd):
    msg = getEncryptMsg()
    return RSAEncode.getEncodeInfo(pwd, msg['exponent'], msg['modulus']) 

def save_cookies(request_cookiejar):
    with open(COOKIE_FILE, 'wb') as f:
        pickle.dump(request_cookiejar, f)

def load_cookies():
    if not os.path.exists(COOKIE_FILE):
        return
    with open(COOKIE_FILE, 'rb') as f:
        return pickle.load(f)


def login(username, pwd):
    pwd = getEncodePwd(pwd)
    payload = {'name':username, 'pwd':pwd}
    r = requestUrl(LOGIN_URL,payload)
    return json.loads(r.text)

def requestUrl(url, data):
    print(HOST + url)
    headers = {'Content-Type':'application/json'}
    cookies = load_cookies();
    data = json.dumps(data)
    r = requests.post(HOST + url, headers=headers, cookies=cookies, data=data)
    save_cookies(r.cookies)
    print(r.text)
    return r

def testUrl():
    requestInfo = loadJsonFromFile(REQUEST_INFO_FILE)
    r = requestUrl(requestInfo['url'], requestInfo['data'])
    result = json.loads(r.text)
    if result['success'] == 'success':
        print(result['data'])
    elif 'NOTLOGIN' in json.dumps(result['data']):
        loginResult = login(USER_NAME, PWD)
        if loginResult['success'] == 'success':
            testUrl()
        else:
            print('login error')
            print(loginResult)
    else:
        print('api error')
        print(result)

testUrl()
