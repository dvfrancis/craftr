from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib import messages


def login_page(request):
    return render(request, 'login/login.html')


class CustomLoginView(LoginView):
    """Custom login view to display messages for login events"""
    def form_valid(self, form):
        messages.success(self.request, "You have been logged in successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Invalid username or password. Please try again."
        )
        return super().form_invalid(form)
