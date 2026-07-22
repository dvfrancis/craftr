from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)


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
            # The sender has to be an address SES is allowed to send as, which
            # EMAIL_USER (a Fastmail login) is not - every message was refused.
            # Enquiries come from and go to the site's own address; replies go
            # to whoever filled the form in.
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.DEFAULT_FROM_EMAIL]
            reply_to_email = [form.cleaned_data.get("email", from_email)]

            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email=from_email,
                to=to_email,
                reply_to=reply_to_email
            )

            # The submission is saved above, so the enquiry is safe whether or
            # not this email gets out - the email only notifies us sooner. The
            # visitor is told it was received either way, because it was;
            # showing them an error would only prompt a duplicate submission.
            # Previously a failure showed the error AND the success message.
            try:
                email.send()
            except Exception as e:
                logger.exception("Contact form notification failed: %s", e)

            messages.success(request, "Your message has been sent")
            return redirect('home')
        else:
            messages.error(request, "Please correct the errors below")
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})
