#!/usr/bin/env python3

import getpass
import requests
from bs4 import BeautifulSoup
import re
#from urllib.parse import unquote

import html

class kaktus:
	def __init__(self):
		self.session = requests.Session()


	def set_proper_headers(self):
		# 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		self.session.headers['Accept-Language'] = 'cs,sk;q=0.8,en-US;q=0.5,en;q=0.3'
		self.session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0'



	def receive_first_cookies(self):
		r = self.session.get('https://www.mujkaktus.cz/moje-sluzby', allow_redirects=False)
		#r.encoding = 'utf-8'
		'''
		cookies = self.session.cookies.get_dict()
		cookies['GUEST_LANGUAGE_ID'] = 'cs_CZ'
		cookies['AJAXIBLE_JAVASCRIPT_ENABLED'] = 'true'
		'''
		print(r.status_code)
		#print(r.history)
		#print(r.reason)
		#print(cookies)

		if r.status_code != 200:
			raise Exception("Status code %d during fething first cookies" % r.status_code)

		self.r = r


	def login(self, username, password):
		'''
		return values:
		 0 - all is OK

		'''

		self.set_proper_headers()
		self.receive_first_cookies()

		data = {}
		data['username'] = username
		data['password'] = password
		data['submit'] = 'Vstoupit'

		#headers = { 'Referer' : 'https://www.mujkaktus.cz/moje-sluzby', 'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-Language' : 'cs,sk;q=0.8,en-US;q=0.5,en;q=0.3', 'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0' }

		print("Log in - POST")
		r = self.session.post('https://www.mujkaktus.cz/.gang/login-url', allow_redirects=False, data = data)
		#r.encoding = 'utf-8'

		
		#print(cookies)

		print(r.status_code)
		print(r.history)
		print(r.reason)

		if r.status_code != 302:
			if "chyby: 701" in r.text:
				raise Exception("Login failed, probably because of 3 incorrect logins")

			else:
				#print(r.text)
				raise Exception("Login failed, unknown reason")

		self.r = r


	def unescape(self, str_i):
		#print(type(str_i))
		#return html.parser.HTMLParser().unescape(str_i)#.encode(), 'utf-8')
		#soup = BeautifulSoup(str_i, "html.parser")
		#return unquote(str_i.decode())
		#print(soup)
		#return soup.pretiffy()
		return html.unescape(str_i.decode())


	def cookies_from_dict(self, dict):
		jar = requests.cookies.RequestsCookieJar()

		for key, value in dict.items():
			jar.set(key, value)

		return jar



	def set_proper_cookies(self):
		cookies = self.session.cookies.get_dict()

		cookies['GUEST_LANGUAGE_ID'] = 'cs_CZ'
		cookies['AJAXIBLE_JAVASCRIPT_ENABLED'] = 'true'

		self.session.cookies = self.cookies_from_dict(cookies)

	


	def set_XHR_header(self):
		self.session.headers['X-Requested-With'] = 'XMLHttpRequest'



	def get_info_url(self):
		print("Getting URL for info - GET")
		r = self.session.get('https://www.mujkaktus.cz/moje-sluzby', allow_redirects=False)

		'''cookies = self.session.cookies.get_dict()
		cookies['GUEST_LANGUAGE_ID'] = 'cs_CZ'
		print(cookies)
		'''
		print(r.status_code)
		print(r.history)
		print(r.reason)
		print(self.unescape(r.content))

		soup = BeautifulSoup(r.content, 'html.parser')
		url = soup.find("div", { "data-invocation-url" : re.compile(r"https://.*") })['data-invocation-url']
		#print(url)
		return url


	def get_info_html(self):
		self.set_proper_cookies()

		url = self.get_info_url()

		self.set_XHR_header()

		r = self.session.get(url, allow_redirects=False)

		print(r.status_code)
		print(r.reason)
		return self.unescape(r.content)


	def logout(self):
		r = self.session.get('https://www.mujkaktus.cz/.gang/logout')
		print(r.status_code)

		self.r = r




cli = kaktus()

import sys
username = sys.argv[1]
password = ""


print("Your kaktus password:")
password = getpass.getpass()



cli.login(username, password)

#print(unescape(r.content))






#self.session, f = get_info_url(self)

#params = { 'p_p_id' : 'kaktusvcc_WAR_vcc', 'p_p_lifecycle' : 2, 'p_p_state' : 'normal', 'p_p_mode' : 'view', 'p_p_cacheability' : 'cacheLevelPage', 'p_p_col_id' : 'column-1', 'p_p_col_pos' : 1, 'p_p_col_count' : 2, '_kaktusvcc_WAR_vcc_userAction' : 'dashboard.enter', '_kaktusvcc_WAR_vcc_from' : 'dashboard', '_kaktusvcc_WAR_vcc_vccDaemonUrl' : 1 }



import datetime
html = cli.get_info_html()

with open("data_%s_log.txt" % str(datetime.datetime.now()).replace(" ", "-"), "w") as f:
	f.write(html)

print(html)

cli.logout()

print(cli.session.headers)