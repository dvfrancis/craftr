from django.shortcuts import render


def faq_page(request):
    """
    Render the FAQ page.

    This view renders the FAQ page template for the application.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered FAQ page.
    """
    return render(request, 'faq/faq.html')
