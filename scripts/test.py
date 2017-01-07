# -*- coding: utf-8 -*-
import re
import urllib2
import requests
import datetime, time, pytz
from bs4 import BeautifulSoup
import parsers
from parsers import urlopen
from django.db.models import Max
from android.models import Android
from iOS.models import IOS
from Mac.models import Mac


cookie4pda = {
	'cf_clearance': '2eecd513e6f9c864ce3afe394edfc532c789b706-1482789489-604800'
	}


def urlopen(url, cookie={}):
	"""Url opener"""
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'}
	page = requests.get(url, headers=headers, cookies=cookie)
	html = page.text.encode('utf-8')
	return BeautifulSoup(html, 'html.parser')



objects = Android.objects.all()
for obj in objects:
	try:

		print(obj.name)
		new = parsers.Android(obj.url).description
		# old = obj.description
		# old = old.replace(". ", ".<br>")
		# old = old.replace("! ", "!<br>")
		obj.description = new
		obj.save()
	except:
		pass
	# print obj.description
	# break


# a = parsers.Android("https://play.google.com/store/apps/details?id=com.game.motorsportmanager").description

# print a
# b = '<br/>'
# print b
# print urlopen("http://4pda.ru/tag/programs-for-ios/", cookie4pda)








# import time
#
#
# pattern = "Asd"
# m = len(pattern)
# skip = []
# for k in range(256):
#     skip.append(m)
# for k in range(m - 1): skip[ord(pattern[k])] = m - k - 1
# skip = tuple(skip)
# print set(skip)

# # @timeout(2)
# def long_running_function1(sec):
#     start_time = time.time()
#     while True:
#         if time.time() - start_time > sec:
#             print 0
#             break
#
#
#
# print long_running_function1(3)
# print long_running_function1(1)



# print re.match("fdsg 1,99", r".(\d.*\d)")



#  b = parsers.urlopen("http://4pda.ru")
# lastdate = Android.objects.filter(source="4pda").aggregate(Max('date')).values()
# print lastdate
# a = Android.objects.order_by('source')[0]
# print Android.objects.all()











# objects = Android.objects.all()
# for obj in objects:
#     old = obj.description
#     old = old.replace(". ", ".<br>")
#     old = old.replace("! ", "!<br>")
#     obj.description = old
#     obj.save()
#     print obj.description
#     break





















#
# def urlopen(url):
#     response = urllib2.urlopen(url)
#     html = response.read()
#     return BeautifulSoup(html, 'html.parser')
#
# # def pars_4pda(url, search_title, lastdate=0):
#
# link = "https://play.google.com/store/apps/details?id=com.pixonic.wwr"
#
# html = urlopen(link)
#
#
#
# b = html.find("div", itemprop="description").contents[1].text
# print b









# obj = parsers.Android(link, "2016-01-16", "4pda")
# obj.toDB()
#
# item = Android(
#     name=obj.name,
#     date=obj.datePublished,
#     url=obj.url,
#     rating=obj.rating,
#     star=obj.star,
#     halfstar=obj.halfstar,
#     price=obj.price,
#     screenshots=obj.screenshots,
#     artist=obj.artist
#     )
# item.save()
# price = html.find("span", class_="display-price").string
# name = html.find("div", class_="id-app-title").string
# artist = html.find("span", itemprop="name").string
# rating = html.find("meta", itemprop="ratingCount").get("content")
# starfloat = float(html.find("div", class_="score").string)
# star = int(starfloat)
# halfstar = int(round(starfloat) - star)
# screenshots = html.find_all("img", itemprop="screenshot")
# # ratings, a = allrating["aria-label"].split(",")
# for i in screenshots[:5]:
#     print i.get("src")
#
#
#
# print price, name, artist, star, halfstar, rating
#
#
# item = Android(
#     name="self.name",
#     date=datetime.date.today(),
#     url="self.url",
#     rating=0,
#     star=0,
#     halfstar=0,
#     price=0,
#     screenshots="self.screenshots",
#     artist="self.artist"
#     )