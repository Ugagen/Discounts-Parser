# -*- coding: utf-8 -*-
import re
import requests
import datetime
import pytz
from bs4 import BeautifulSoup


def urlopen(url, cookie={}):
    """Url opener"""
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:50.0) Gecko/20100101 Firefox/50.0'}
    page = requests.get(url, headers=headers, cookies=cookie)
    html = page.text.encode('utf-8')
    return BeautifulSoup(html, 'html.parser')


def time_transformation(date):
    """transformation time to full time format
    example:
    time_transformation("6 hours ago")
    > 2016-04-11 15:57:43.624871"""
    nowDate = datetime.datetime.now().replace(tzinfo=pytz.utc)
    if "minute" in date:
        date = int(re.match("([\d]).*", date).group(1))
        return nowDate - datetime.timedelta(minutes=date)
    elif "hour" in date:
        date = int(re.match("([\d]).*", date).group(1))
        return nowDate - datetime.timedelta(hours=date)
    elif "day" in date:
        date = int(re.match("([\d]).*", date).group(1))
        return nowDate - datetime.timedelta(days=date)
    elif "week" in date:
        date = int(re.match("([\d]).*", date).group(1))
        return nowDate - datetime.timedelta(days=date * 7)


def pars_4pda(url, search_title, cookie={}, lastdate=0):
    """Parser 4pda.ru
    The site has a parser protector. For bypass validation needed latest version a user-agent and sometimes cookies.
    search_title - It is a pattern for search in titles.
    lastdate - It is the date of the last update in the DB, this is needed to stop script on the place where was the last parsing.
    The script returns a dictionary {"url": {"datePublished", "source"}} """
    soup = urlopen(url, cookie)
    pages = soup.find_all(title=search_title)
    sales_list = []
    for page in pages:
        if page.get("itemprop") == None and page.get('href') != None:
            link = str(page.get('href'))
            sales_list.append(link)
    sales_dict = {}
    for url in sales_list:
        soup = urlopen(url, cookie)
        datePublished = soup.find("meta", itemprop="datePublished").get('content')[:10]
        if datePublished == lastdate[:10]:
            break
        links = soup.find_all(class_="mlinks")
        for link in links:
            url = link.find(target="_blank").get("href")
            sales_dict[url] = {"date": datePublished, "source": "4pda"}
        errorlinks =[]
        if "ios" in url:
            errorlinks = soup.find_all("a", target="_blank", href=re.compile("^https://itunes.apple."))
        elif "android" in url:
            errorlinks = soup.find_all("a", target="_blank", href=re.compile("^https://play.google."))
        for link in errorlinks:
            url = link.get("href")
            sales_dict[url] = {"date": datePublished, "source": "4pda"}
    return sales_dict  # {"url": {"datePublished", "source"}}


def pars_appshopper(url, lastdate=None):
    """Parser appshopper.com
    lastdate - It is the date of the last update in the DB, this is needed to stop script on the place where was the last parsing.
    The script returns the dictionary {"url": {"datePublished", "source"}} """
    soup = urlopen(url)
    sales_dict = {}
    sales_list = soup.find_all("span", class_="change-capsule drop")
    for sale in sales_list:
        appObj = sale.parent.parent.parent.parent.parent
        itunes_id = appObj.get("data-appid")
        itunes_url = "https://itunes.apple.com/app/id" + itunes_id
        datePublished = appObj.find("span", class_="last-updated").string
        datePublished = time_transformation(datePublished)
        if lastdate is not None and lastdate >= datePublished:
            break
        sales_dict[itunes_url] = {"date": datePublished, "source": "appshopper"}
    return sales_dict


class Itunes(object):
    """Itunes object"""

    def __init__(self, url, datePublished="", source=""):
        self.url = self.shortLink(url)
        self.datePublished = datePublished
        self.source = source
        self.html = urlopen(self.url)
        self.rating = 0
        self.star = 0
        self.halfstar = 0
        self.price = 0.0
        if self.validation_url() == False:
            self.url = None
        else:
            self.getValues()  # start parsing

    def shortLink(self, url):
        """Get a short link without regional bindings"""
        ApId = re.match(".*(id\d*)", url).group(1)
        shortUrl = "https://itunes.apple.com/app/" + ApId
        return shortUrl

    def validation_url(self):
        """Check the validity of links"""
        title = "Connecting to the iTunes Store."
        if self.html.title.text == title:
            print self.url
            return False
        return True

    def getValues(self):
        """Get values fot the object"""

        """Price parser"""
        try:
            price = self.html.find("div", itemprop="price").get("content")
        except:
            print self.url
        try:
            """if a price is free or not valid, It will "0" """
            self.price = float(price[1:])
        except:
            pass

        """Name parser"""
        self.name = self.html.find("h1", itemprop="name").string

        """Rating parser"""
        try:
            allrating = self.html.find("div", text="All Versions:").nextSibling.nextSibling
            ratings = allrating["aria-label"].split(",")
            self.rating = int(ratings[1].split()[0])
            self.star = int(ratings[0].split()[0])
            if ratings[0].split()[1] == "and":
                self.halfstar = 1
        except:
            pass

        """Screenshot parser"""
        screenCont = self.html.find("div", class_=re.compile(".*screenshots$"))
        screenshotlist = []
        screenshot = "Screenshot "
        if screenCont.find("img", alt=screenshot + "1") == None:
            screenshot = "iPad Screenshot "
            if screenCont.find("img", alt=screenshot + "1") == None:
                screenshot = "iPhone Screenshot "
        for num in range(1, 6):
            try:
                img = self.html.find("img", alt=screenshot + str(num)).get("src")
                screenshotlist.append(img)
            except:
                break
        self.screenshots = " , ".join(screenshotlist)

        """Artist parser"""
        try:
            self.artist = self.html.find(attrs={"preview-artist": True}).get("preview-artist")
        except:
            self.artist = self.html.find("span", itemprop="name").text
        """Description parser"""
        description = self.html.find("p", itemprop="description").getText(separator='nextlineAK')
        # description = description.replace("|next|", '<br/>') 
        self.description = description

    def __str__(self):
        return self.description


class Android(object):
    """Android object"""

    def __init__(self, url, datePublished = "", source = ""):
        self.url = url
        self.datePublished = datePublished
        self.source = source
        self.rating = 0
        self.star = 0
        self.halfstar = 0
        self.price = 0.0
        self.getValues()

    def getValues(self):
        html = urlopen(self.url)

        """Price parser"""
        price = html.find("meta", itemprop="price").get("content")[-4:]
        if price != "FREE":
            price = price.replace(",", ".")
            try:
                self.price = float(price)
            except:
                self.url

        """Name parser"""
        self.name = html.find("div", class_="id-app-title").string

        """Rating parser"""
        try:
            rating = html.find("meta", itemprop="ratingCount").get("content")
            self.rating = int(rating)
            starfloat = float(html.find("div", class_="score").string)
            self.star = int(starfloat)
            self.halfstar = int(round(starfloat) - star)
        except:
            pass

        """Screenshots parser"""
        screenshots = html.find_all("img", itemprop="screenshot")
        screenshotslist = []
        for screenshot in screenshots:
            screenshotslist.append(screenshot.get("src"))
        self.screenshots = " , ".join(screenshotslist[:5])

        """Artist parser"""
        self.artist = html.find("span", itemprop="name").string

        """Description parser"""
        description = html.find("div", itemprop="description").contents[1].getText(separator='nextlineAK')
        # description = "".join(description)
        self.description = description #(separator='nextlineAK')

    def __str__(self):
        return self.url


if __name__ == "__main__":
    pass
