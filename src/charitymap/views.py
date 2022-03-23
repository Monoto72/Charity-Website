from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

def index(request):
    text = "Testing"
    context = {
        'context_text' : text,
    }
    return render(request, 'home.html', context)
    

def error_response(request, exception):
    return render(request, '404.html')


class AboutPageView(TemplateView):  # new
    template_name = "about.html"