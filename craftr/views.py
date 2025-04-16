from django.shortcuts import render


def custom_404(request, exception=None):
    """
    Render the custom 404 error page.

    This view handles 404 errors and renders a custom 404 error page.

    Args:
        request: The HTTP request object.
        exception: The exception that triggered the 404 error (optional).

    Returns:
        HttpResponse: The rendered 404 error page with a 404 status code.
    """
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Render the custom 500 error page.

    This view handles 500 errors and renders a custom 500 error page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered 500 error page with a 500 status code.
    """
    return render(request, "500.html", status=500)
