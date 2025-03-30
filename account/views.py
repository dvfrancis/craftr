from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView

@login_required
def user_details(request):
    return render(
        request,
        "account/account.html",
        {"user": request.user}
    )


def custom_logout(request):
    logout(request)
    return redirect('home')
