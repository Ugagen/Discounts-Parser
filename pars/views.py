from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


# Create your views here.
def index(request):
    sections = ['iOS', 'Mac', 'Android', 'Test']
    template = loader.get_template('Pars/index.html')
    context = RequestContext(request, {
        'sections': sections,
    })
    return HttpResponse(template.render(context))
