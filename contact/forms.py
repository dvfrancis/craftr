from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    """
    Form for handling contact form submissions.

    This form is based on the Contact model and includes fields for the
    user's first name, last name, email, and message. Custom widgets are
    used to provide placeholders and styling for the form fields.

    Meta:
        model (Model): The model associated with the form.
        fields (list): The fields to include in the form.
        widgets (dict): Custom widgets for form fields.
    """
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Enter your first name'}
            ),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Enter your last name'}
            ),
            'email': forms.TextInput(
                attrs={'placeholder': 'Enter your email address'}
            ),
            'message': forms.TextInput(
                attrs={
                    'class': 'contact-textarea',
                    'placeholder': 'Enter your message',
                }
            ),
        }
