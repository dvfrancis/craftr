from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import ContactForm
from django.contrib import messages
import os
from django.conf import settings


def contact_page(request):
    """
    Handle the contact page form submission safely for development.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Build email content
            email_subject = "Craftr Contact Form Submission"
            email_body = (
                f"Name: {form.cleaned_data.get('first_name', '')} "
                f"{form.cleaned_data.get('last_name', '')}\n"
                f"Email: {form.cleaned_data.get('email', '')}\n"
                f"Message: {form.cleaned_data.get('message', '')}"
            )
            # Use safe from_email fallback
            from_email = os.getenv("EMAIL_USER") or "no-reply@example.com"
            to_email = [os.getenv("EMAIL_USER") or "no-reply@example.com"]
            reply_to_email = [form.cleaned_data.get("email", from_email)]

            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=from_email,
                to=to_email,
                reply_to=reply_to_email
            )

            # Try sending the email safely
            try:
                email.send()
                print("Email sent successfully (or printed to console in dev)")
            except Exception as e:
                print("Email sending error:", e)

            messages.success(request, "Your message has been sent")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})
