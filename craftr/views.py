from django.shortcuts import render
from django.http import Http404


def test_404(request):
    raise Http404()