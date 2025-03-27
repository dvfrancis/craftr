from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def faq(request):
    return HttpResponse("This is the faq page")