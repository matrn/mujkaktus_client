#!/usr/bin/env python3

from bs4 import BeautifulSoup

soup = BeautifulSoup(t, 'html.parser')
text_1 = soup.findAll("span", { "class" : "text-1" })
text_2 = soup.findAll("span", { "class" : "text-2" })

credit = text_1[0]
currency = text_2[0]

span = soup.findAll("span")
p = soup.findAll("p")


credit = ""
credit_unit = "Kč"
credit_expire = ""
credit_expire_unit = "Platnost do"

minutes = ""
minutes_unit = "minut"
minutes_type = ""

sms = ""
sms_unit = "SMS"
sms_type = ""

mb_normal = ""
mb_social = ""
mb_type = ""

renew_keyword = "samoobnov"
once_keyword = "jednor"

#print(span)
prev = ""
for elm in p:
	if len(elm.text) != 0:
		print(elm)
		
		elm_s = str(elm)
		#s = BeautifulSoup(elm, "html.parser")

		if credit_unit.lower() in elm_s.lower():   #credit
			credit = str(elm.find("span", { "class" : "text-1"}).text).lstrip()
			prev = "credit"
		
		if credit_expire_unit.lower() in elm_s.lower() and len(credit) != 0:   #credit expiration
			credit_expire = str(elm.text).replace(credit_expire_unit, "").lstrip()
			prev = "credit"


		if minutes_unit.lower() in elm_s.lower():   #minutes
			minutes = str(elm.find("span", { "class" : "text-2"}).text).lstrip()
			prev = "mins"


		if sms_unit.lower() in elm_s.lower():   #minutes
			sms = str(elm.find("span", { "class" : "text-2"}).text).lstrip()
			prev = "sms"


		if renew_keyword.lower() in elm_s.lower() or once_keyword.lower() in elm_s.lower():
			if prev == "mins": minutes_type = renew_keyword
			if prev == "sms": sms_type = renew_keyword

			prev = "type"



print("Credit: " + credit + " " + credit_unit)
print("Credit expiration: " + credit_expire)

print("Minutes: " + minutes + " " + minutes_unit + " " + minutes_type)
print("SMS: " + sms + " " + sms_unit + " " + sms_type)
#print(text_1)
#print(text_2)