import requests, requests.utils, pickle
import selenium.webdriver 
import time
import re
import hashlib

s = requests.session()
s.cookies.clear()


def try_restart():
	global s
	print('try restart')
	rr = s.get('http://att.mifiliberate/cgi/webui.cgi?id=restarting')
	if rr:
		gSecureToken = re.findall('{ gSecureToken: "(.*)" }', rr.text)
		if gSecureToken:
			xx = s.post('http://att.mifiliberate/cgi/webui.cgi?id=restarting&as=1&reboot=true', {
				'gSecureToken': gSecureToken[0]
			});	
			
			print(gSecureToken[0])
			print(xx)
		else:
			print(gSecureToken)
	else:
		print(rr.text)
		
login = s.get('http://att.mifiliberate/login')
if login:
	secToken = re.findall('secToken = "(.*)";', login.text)
	if secToken:
		secToken = secToken[0]
		inputPw = 'attadmin'
		
		sh = hashlib.sha1()
		sh.update(str(inputPw + secToken).encode('utf-8'))
		shaPw = sh.hexdigest()
		
		params = dict()
		params['redirectLocation'] = 'http://att.mifiliberate/'
		params['shaPassword'] = shaPw
		params['inputPassword'] = secToken[0:len(inputPw)]
		
		print(params)
		
		process = s.post('http://att.mifiliberate/login', params)
		print(process.text)
		
		try_restart()
	else:
		if 'Logout' in login.text:
			print('Already logged in?')
			try_restart()
		else:
			print(login.text)

	