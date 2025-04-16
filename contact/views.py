from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.contrib import messages
import os


def contact_page(request):
    """
    Handle the contact page form submission.

    This view processes the contact form, saves the data to the database,
    sends an email with the form details, and provides feedback to the user.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered contact page with the form or a redirect
        to the home page after successful submission.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            email = EmailMessage(
                subject="Craftr Contact Form Submission",
                body=(
                    f"Name: {form.cleaned_data['first_name']} "
                    f"{form.cleaned_data['last_name']}\n"
                    f"Email: {form.cleaned_data['email']}\n"
                    f"Message: {form.cleaned_data['message']}"
                ),
                from_email=os.getenv("EMAIL_USER"),
                to=[os.getenv("EMAIL_USER")],
                reply_to=[form.cleaned_data["email"]],
            )
            email.send()
            messages.success(request, "Your message has been sent")
            return redirect('home')
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})
