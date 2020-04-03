# -*- coding: utf-8 -*-
import time
import random
import pymongo
import urllib3
import requests
from urllib import request
from bs4 import BeautifulSoup
from pymongo import MongoClient
from bson.objectid import ObjectId
import threading
import aiohttp
import asyncio

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

client=MongoClient('localhost',27017)
db=client.ProxyPool
pool = db['Pool']


def header():
	headers = {
		'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
	    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
	    'Accept-Encoding':'gzip, deflate, br',
	    'Connection':'keep-alive',
	    'Upgrade-Insecure-Requests':'1',
	    }
	return headers

async def get_url(url,web_name):
		async with aiohttp.ClientSession() as session:
			async with session.get(url, headers = header(), verify_ssl=False) as resp:
				if resp.status == 200:
					url_true.append(url)
				else:
					url_false.append(url)		
				html = await resp.text()
				soup = BeautifulSoup(html, 'html.parser')
				choice_web(web_name,soup)

def get_xici(soup):
	tr = soup.find_all('tr')
	# Search proxy data from web #
	for td in tr[1:]:
		ip = td.find_all('td')[1].get_text()
		port = td.find_all('td')[2].get_text()
		types = td.find_all('td')[5].get_text()
		speed = td.find_all('td')[6].find('div').get('title')
		connect = td.find_all('td')[7].find('div').get('title')
		live = td.find_all('td')[8].get_text()
		if types == 'HTTPS' :
			proxy = 'https://' + ip + ':' + port
			cut = 'https'
		else:
			proxy = 'http://' + ip + ':' + port
			cut = 'http'
		# Save proxy data #

		db.Pool.insert_many([{
			'Proxy' : proxy,
			'Type' : cut
			}])

def get_xila(soup):
	tr = soup.find_all('tr')
	# Search proxy data from web #
	for td in tr[1:]:
		ip = td.find_all('td')[0].get_text()
		types = td.find_all('td')[1].get_text()
		speed = td.find_all('td')[4].get_text()
		live = td.find_all('td')[5].get_text()
		rank = td.find_all('td')[7].get_text()
		if types == 'HTTPS代理' :
			proxy = 'https://' + ip
			cut = 'https'

		elif types == 'HTTP代理' :
			proxy = 'http://' + ip
			cut = 'http'

		else:
			proxy = 'https://' + ip
			cut = 'https'
		# Save proxy data #
		db.Pool.insertmany([{	
			'Proxy' : proxy,
			'Type' : cut
			}])

def get_66ip(soup):
	tr = soup.find_all('tr')
	# Search proxy data from web #
	for td in tr[2:]:
		ip = td.find_all('td')[0].get_text()
		port = td.find_all('td')[1].get_text()
		
def get_kuai(soup):
	tr = soup.find_all('tr')
	# Search proxy data from web #
	for td in tr[1:]:
		ip = td.find_all('td')[0].get_text()
		port = td.find_all('td')[1].get_text()
		types = td.find_all('td')[3].get_text()
		speed = td.find_all('td')[5].get_text()
		if types == 'HTTPS' :
			proxy = 'https://' + ip + ':' + port
			cut = 'https'
		else:
			proxy = 'http://' + ip + ':' + port
			cut = 'http'
		# Save proxy data #
		db.Pool.insert_one([{	
			'Proxy' : proxy,
			'Type' : cut
			}])

def get_yun(soup):
	tr = soup.find_all('tr')
	# Search proxy data from web #
	for td in tr[1:]:
		ip = td.find_all('td')[0].get_text()
		port = td.find_all('td')[1].get_text()
		types = td.find_all('td')[3].get_text()
		speed = td.find_all('td')[6].get_text()
		if types == 'HTTPS' :
			proxy = 'https://' + ip + ':' + port
			cut = 'https'
		else:
			proxy = 'http://' + ip + ':' + port
			cut = 'http'
		# Save proxy data #
		db.Pool.insert_one([{	
			'Proxy' : proxy,
			'Type' : cut
			}])

def choice_web(web_name,soup):
	if web_name == 'xici' :
		get_xici(soup)
	elif web_name == 'xila' :
		get_xila(soup)
	elif web_name == '66ip' :
		get_66ip(soup)
	elif web_name == 'kuai' :
		get_kuai(soup)
	elif web_name == 'yun' :
		get_yun(soup)



		
urls = ['https://www.xicidaili.com/nn/%d'%i for i in range(1,20)]
url_true = []
url_false = []

tasks = [asyncio.ensure_future(get_url(url,'xici')) for url in urls]
loop = asyncio.get_event_loop()
time.sleep(30)
loop.run_until_complete(asyncio.wait(tasks))

# ----分割线---- #
