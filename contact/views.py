from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.contrib import messages
import os


def contact_page(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save to database
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
            messages.success(request, "Contact form submitted successfully!")
            return redirect('home')  # Redirect after submission
    else:
        form = ContactForm()
    return render(request, "contact/contact.html", {"form": form})
    