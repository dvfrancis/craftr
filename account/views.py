from django.shortcuts import render


def account_page(request):
    return render(request, 'account/account.html')