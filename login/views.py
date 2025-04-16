from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib import messages


def login_page(request):
    """
    Render the login page.

    This view renders the login page template for users to enter their
    credentials.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered login page.
    """
    return render(request, 'login/login.html')


class CustomLoginView(LoginView):
    """
    Custom login view to display messages for login events.

    This class extends Django's built-in LoginView to add success and error
    messages for login attempts.
    """
    def form_valid(self, form):
        """
        Handle successful login attempts.

        Displays a success message when the user logs in successfully.

        Args:
            form: The submitted login form.

        Returns:
            HttpResponse: The response from the parent form_valid method.
        """
        messages.success(self.request, "You have been logged in successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle failed login attempts.

        Displays an error message when the login attempt fails.

        Args:
            form: The submitted login form.

        Returns:
            HttpResponse: The response from the parent form_invalid method.
        """
        messages.error(
            self.request,
            "Invalid username or password. Please try again."
        )
        return super().form_invalid(form)
