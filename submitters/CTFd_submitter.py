#!--encoding=utf-8--

# 请按照 [题目id]\[flag] 的格式提交
# 如challenge_id为1，flag为flag{123-123}则attack函数返回 "1\flag{123-123}"

from yaml import safe_load
import submitters
import re
import requests
import time

class CTFdSubmitter(submitters.Submitter):
    nonce_re = re.compile(r'var csrf_nonce = "(.*)"')
    nonce_new = re.compile(r'\'csrfNonce\': "(.*)",')
    _header = {
        'Accept-Language': 'en-US,en;q=0.5',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:69.0) Gecko/20100101 Firefox/69.0'
    }

    def __init__(self, url, username=None, password=None):
        self.url = url
        self.ses = requests.session()
        self.ses.headers.update(self._header)
        if username:
            self.login(username, password)

    def _extract_token(self, text):
        try:
            self.ses.headers.pop('CSRF-Token')
        except:
            pass
        try:
            nonce = self.nonce_re.findall(text)[0]
        except:
            nonce = self.nonce_new.findall(text)[0]
        self.ses.headers.setdefault('CSRF-Token', nonce)

    def login(self, username, passwd):
        self._extract_token(self.ses.get(self.url+'/login').text)
        self._extract_token(self.ses.post(self.url+'/login', data={
            'name': username,
            'password': passwd,
            'nonce': self.ses.headers.get('CSRF-Token'),
        }).text)

    def submit(self, answer):
        chall, answer = answer.split('\\')
        x = self.ses.post(self.url+'/api/v1/challenges/attempt', json={
            'challenge_id': chall,
            'submission': answer
        }).json()
        if 'data' in x.keys():
            if x['data']['status'] == 'ratelimited':
                time.sleep(10)
                return self.submit(chall+'\\'+answer)
            elif x['data']['status'] == 'incorrect':
                return 'wrong'
            elif x['data']['status'] == 'correct' or x['data']['status'] == 'already_solved':
                return 'success'
            return x['data']['status']
        return 'submit_error'
