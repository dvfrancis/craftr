from django.shortcuts import render


def details_page(request):
    return render(request, 'details/details.html')
