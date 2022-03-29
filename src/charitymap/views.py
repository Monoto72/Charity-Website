from django.shortcuts import render
from django.views.generic import TemplateView
from json import dumps
from charitymap.models import Store

# Create your views here.

def index(request):
    text = "Testing"
    context = {
        'context_text' : text,
    }
    return render(request, 'home.html', context)


def test(request):  # new
    data = Store.objects.get(pk=1)
    return render(request, 'test.html', { data: data })


def error_response(request, exception):
    return render(request, '404.html')


class AboutPageView(TemplateView):  # new
    template_name = "about.html"