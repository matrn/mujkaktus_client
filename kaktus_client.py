#!/usr/bin/env python3

import getpass
import requests
from bs4 import BeautifulSoup
import re
#from urllib.parse import unquote

import html

def unescape(str_i):
	#print(type(str_i))
	#return html.parser.HTMLParser().unescape(str_i)#.encode(), 'utf-8')
	#soup = BeautifulSoup(str_i, "html.parser")
	#return unquote(str_i.decode())
	#print(soup)
	#return soup.pretiffy()
	return html.unescape(str_i.decode())

def cookies_from_dict(dict):
	jar = requests.cookies.RequestsCookieJar()

	for key, value in dict.items():
		jar.set(key, value)

	return jar

username = ""
password = ""


print("Your kaktus password:")
password = getpass.getpass()


session = requests.Session()


headers = { 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language' : 'cs,sk;q=0.8,en-US;q=0.5,en;q=0.3', 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0' }


print("First request - GET")
r = session.get('https://www.mujkaktus.cz', allow_redirects=False, headers = headers)
r.encoding = 'utf-8'

cookies = session.cookies.get_dict()
cookies['GUEST_LANGUAGE_ID'] = 'cs_CZ'
cookies['AJAXIBLE_JAVASCRIPT_ENABLED'] = 'true'
print(r.status_code)
print(r.history)
print(r.reason)
print(cookies)
#print(unescape(r.content))

data = {}
data['username'] = username
data['password'] = password
data['submit'] = 'Vstoupit'

headers = { 'Referer' : 'https://www.mujkaktus.cz/moje-sluzby', 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language' : 'cs,sk;q=0.8,en-US;q=0.5,en;q=0.3', 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0' }

print("Log in - POST")
r = session.post('https://www.mujkaktus.cz/.gang/login', allow_redirects=False, headers = headers, cookies = cookies, data = data)
r.encoding = 'utf-8'

cookies = session.cookies.get_dict()
cookies['GUEST_LANGUAGE_ID'] = 'cs_CZ'
cookies['AJAXIBLE_JAVASCRIPT_ENABLED'] = 'true'
session.cookies = cookies_from_dict(cookies)
print(cookies)

print(r.status_code)
print(r.history)
print(r.reason)
#print(unescape(r.content))


print("Getting URL for info - GET")
r = session.get('https://www.mujkaktus.cz/moje-sluzby', allow_redirects=False, headers = headers)

cookies = session.cookies.get_dict()
cookies['GUEST_LANGUAGE_ID'] = 'cs_CZ'
print(cookies)

print(r.status_code)
print(r.history)
print(r.reason)
print(unescape(r.content))
soup = BeautifulSoup(r.content, 'html.parser')
f = soup.find("div", { "data-invocation-url" : re.compile(r"https://.*") })['data-invocation-url']
print(f)




headers['X-Requested-With'] = 'XMLHttpRequest'
#params = { 'p_p_id' : 'kaktusvcc_WAR_vcc', 'p_p_lifecycle' : 2, 'p_p_state' : 'normal', 'p_p_mode' : 'view', 'p_p_cacheability' : 'cacheLevelPage', 'p_p_col_id' : 'column-1', 'p_p_col_pos' : 1, 'p_p_col_count' : 2, '_kaktusvcc_WAR_vcc_userAction' : 'dashboard.enter', '_kaktusvcc_WAR_vcc_from' : 'dashboard', '_kaktusvcc_WAR_vcc_vccDaemonUrl' : 1 }

r = session.get(f, allow_redirects=False, headers = headers, cookies = cookies)
print(r.status_code)
print(r.reason)
print(unescape(r.content))

def login(session, email, password):
	'''
	return values:
	 0 - all is OK

	'''

