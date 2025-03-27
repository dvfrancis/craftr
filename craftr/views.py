from django.shortcuts import render


def home_page(request):
    return render(request, 'home/index.html')


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)