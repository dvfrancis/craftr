from django.shortcuts import render


def home_page(request):
    """
    Render the home page.

    This view renders the home page template for the application.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.
    """
    return render(request, 'home/index.html/')
