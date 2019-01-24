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



def set_proper_cookies(session):
	cookies = session.cookies.get_dict()

	cookies['GUEST_LANGUAGE_ID'] = 'cs_CZ'
	cookies['AJAXIBLE_JAVASCRIPT_ENABLED'] = 'true'

	session.cookies = cookies_from_dict(cookies)

	return session



def set_proper_headers(session):
	# 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	session.headers['Accept-Language'] = 'cs,sk;q=0.8,en-US;q=0.5,en;q=0.3'
	session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'

	return session



def set_XHR_header(session):
	session.headers['X-Requested-With'] = 'XMLHttpRequest'
	return session



def receive_first_cookies(session):
	r = session.get('https://www.mujkaktus.cz/moje-sluzby', allow_redirects=False)
	#r.encoding = 'utf-8'
	'''
	cookies = session.cookies.get_dict()
	cookies['GUEST_LANGUAGE_ID'] = 'cs_CZ'
	cookies['AJAXIBLE_JAVASCRIPT_ENABLED'] = 'true'
	'''
	print(r.status_code)
	#print(r.history)
	#print(r.reason)
	#print(cookies)

	return session



def login(session, username, password):
	'''
	return values:
	 0 - all is OK

	'''
	data = {}
	data['username'] = username
	data['password'] = password
	data['submit'] = 'Vstoupit'

	#headers = { 'Referer' : 'https://www.mujkaktus.cz/moje-sluzby', 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language' : 'cs,sk;q=0.8,en-US;q=0.5,en;q=0.3', 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0' }

	print("Log in - POST")
	r = session.post('https://www.mujkaktus.cz/.gang/login', allow_redirects=False, data = data)
	#r.encoding = 'utf-8'

	
	#print(cookies)

	print(r.status_code)
	print(r.history)
	print(r.reason)

	return session

def get_info_url(session):
	print("Getting URL for info - GET")
	r = session.get('https://www.mujkaktus.cz/moje-sluzby', allow_redirects=False)

	'''cookies = session.cookies.get_dict()
	cookies['GUEST_LANGUAGE_ID'] = 'cs_CZ'
	print(cookies)
	'''
	print(r.status_code)
	print(r.history)
	print(r.reason)
	#print(unescape(r.content))
	soup = BeautifulSoup(r.content, 'html.parser')
	url = soup.find("div", { "data-invocation-url" : re.compile(r"https://.*") })['data-invocation-url']
	#print(url)
	return session, url


def logout(session):
	r = session.get('https://www.mujkaktus.cz/.gang/logout')
	print(r.status_code)

	return session



username = ""
password = ""


print("Your kaktus password:")
password = getpass.getpass()

session = requests.Session()





session = set_proper_headers(session)
session = receive_first_cookies(session)
session = login(session, username, password)

session = set_proper_cookies(session)
#print(unescape(r.content))






session, f = get_info_url(session)
session = set_XHR_header(session)
#params = { 'p_p_id' : 'kaktusvcc_WAR_vcc', 'p_p_lifecycle' : 2, 'p_p_state' : 'normal', 'p_p_mode' : 'view', 'p_p_cacheability' : 'cacheLevelPage', 'p_p_col_id' : 'column-1', 'p_p_col_pos' : 1, 'p_p_col_count' : 2, '_kaktusvcc_WAR_vcc_userAction' : 'dashboard.enter', '_kaktusvcc_WAR_vcc_from' : 'dashboard', '_kaktusvcc_WAR_vcc_vccDaemonUrl' : 1 }

r = session.get(f, allow_redirects=False)
print(r.status_code)
print(r.reason)
print(unescape(r.content))


session, f = get_info_url(session)
r = session.get(f, allow_redirects=False)
print(r.status_code)
print(r.reason)
print(unescape(r.content))

logout(session)

print(session.headers)