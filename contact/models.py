from django.db import models


class Contact(models.Model):
    """
    Represents a contact form submission.

    This model stores information submitted through the contact form,
    including the user's name, email, message, and the timestamp of
    when the submission was created.

    Attributes:
        first_name (CharField): The first name of the user.
        last_name (CharField): The last name of the user.
        email (EmailField): The email address of the user.
        message (TextField): The message submitted by the user.
        created_at (DateTimeField): The timestamp when the submission was
        created.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the contact submission.

        Returns:
            str: The full name of the user who submitted the form.
        """
        return (f"{self.first_name} {self.last_name}")
