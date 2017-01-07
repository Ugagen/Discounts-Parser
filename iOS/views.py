from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from .models import IOS


def datetime_toDate(datetime):
    """Convert datetime format to date"""
    return datetime.replace(hour=0, minute=0, second=0, microsecond=0)


# Create your views here.

def index(request):
    sale_list = IOS.objects.order_by('-date')
    template = loader.get_template('ios/index.html')
    dates = []
    count = 0
    for obj in sale_list:
        date = datetime_toDate(obj.date)
        if date not in dates:
            dates.append(date)
            count += 1
        if count > 15:
            break
    context = RequestContext(request, {
        'dates': dates,
    })
    return HttpResponse(template.render(context))


def dates(request, date):
    date = date.split("_")
    sale_list = IOS.objects.filter(date__year=date[0],
                         date__month=date[1],
                         date__day=date[2]).order_by("price", "-star", "-halfstar", "-rating")
    template = loader.get_template('item.html')
    context = RequestContext(request, {
        'sale_list': sale_list,
    })
    return HttpResponse(template.render(context))
