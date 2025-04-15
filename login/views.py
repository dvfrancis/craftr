from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib import messages


def login_page(request):
    return render(request, 'login/login.html')


class CustomLoginView(LoginView):
    """Display message upon successful login"""
    def form_valid(self, form):
        messages.success(self.request, "You have been logged in successfully!")
        return super().form_valid(form)
