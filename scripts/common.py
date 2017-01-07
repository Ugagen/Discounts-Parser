# -*- coding: utf-8 -*-
import re
import parsers
from django.db.models import Max
from iOS.models import IOS
from android.models import Android
from Mac.models import Mac

cookie4pda = {
    'cf_clearance': '2eecd513e6f9c864ce3afe394edfc532c789b706-1482789489-604800'
    }


def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z


def parsIOS():
    """Parsing 4pda"""
    url_4pda = 'http://4pda.ru/tag/games-for-ios/'
    search_title = re.compile(r"^Скидки на+".decode('utf-8'))
    lastdate_4pda = IOS.objects.filter(source="4pda").aggregate(Max('date')).values()[0]
    lastdate_4pda = unicode(lastdate_4pda)
    itunes_4pda = parsers.pars_4pda(url_4pda, search_title, cookie4pda, lastdate_4pda)

    """Parsing appshopper"""
    url_appshopper = "http://appshopper.com/"
    lastdate_appshopper = IOS.objects.filter(source="appshopper").aggregate(Max('date')).values()[0]
    itunes_appshopper = parsers.pars_appshopper(url_appshopper, lastdate_appshopper)
    itunes_links = merge_two_dicts(itunes_appshopper, itunes_4pda)
    return itunes_links


def iosToDB():
    itunes_links = parsIOS()
    for link in itunes_links:
        obj = parsers.Itunes(link, itunes_links[link]["date"], itunes_links[link]["source"])
        if obj.url is not None:
            item = IOS(
                name=obj.name,
                date=obj.datePublished,
                url=obj.url,
                rating=obj.rating,
                star=obj.star,
                halfstar=obj.halfstar,
                price=obj.price,
                screenshots=obj.screenshots,
                artist=obj.artist,
                description=obj.description,
                source=obj.source
                )
            item.save()


def parsAndroid():
    url = 'http://4pda.ru/tag/games-for-android/'
    search_title = re.compile(r"^Скидки на+".decode('utf-8'))
    lastdate = Android.objects.filter(source="4pda").aggregate(Max('date')).values()[0]
    lastdate = unicode(lastdate)
    android_links = parsers.pars_4pda(url, search_title, cookie4pda, lastdate)
    return android_links


def androidToDB():
    android_links = parsAndroid()
    for link in android_links:
        obj = parsers.Android(link, android_links[link]["date"], android_links[link]["source"])
        item = Android(
            name=obj.name,
            date=obj.datePublished,
            url=obj.url,
            rating=obj.rating,
            star=obj.star,
            halfstar=obj.halfstar,
            price=obj.price,
            screenshots=obj.screenshots,
            artist=obj.artist,
            description=obj.description,
            source=obj.source
            )
        item.save()


def parsMac():
    url_appshopper = "http://appshopper.com/mac"
    lastdate_appshopper = Mac.objects.filter(source="appshopper").aggregate(Max('date')).values()[0]
    itunes_appshopper = parsers.pars_appshopper(url_appshopper, lastdate_appshopper)
    return itunes_appshopper


def MacToDB():
    itunes_links = parsMac()
    for link in itunes_links:
        obj = parsers.Itunes(link, itunes_links[link]["date"], itunes_links[link]["source"])
        item = Mac(
            name=obj.name,
            date=obj.datePublished,
            url=obj.url,
            rating=obj.rating,
            star=obj.star,
            halfstar=obj.halfstar,
            price=obj.price,
            screenshots=obj.screenshots,
            artist=obj.artist,
            description=obj.description,
            source=obj.source
            )
        item.save()


def datetime_toDate(datetime):
    """Convert datetime format to date"""
    return datetime.replace(hour=0, minute=0, second=0, microsecond=0)


def del_dublicates(model):
    objects = model.objects.order_by('-date')
    dates = []
    count = 0
    for obj in objects:
        date = datetime_toDate(obj.date)
        if date not in dates:
            dates.append(date)
            count += 1
        if count > 15:
            break
    for date in dates:
        sales = model.objects.filter(date__year=date.year,
                                    date__month=date.month,
                                    date__day=date.day)
        items = sales.values_list('url')
        for item in items:
            temp = sales.filter(url__iexact=item)
            if len(temp) > 1:
                for i in temp[1:]:
                    i.delete()



# if __name__ == "__main__":
iosToDB()
androidToDB()
MacToDB()
del_dublicates(IOS)
del_dublicates(Android)
del_dublicates(Mac)
