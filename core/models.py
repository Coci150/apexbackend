# core/models.py
from django.db import models
from django.core.validators import EmailValidator


class Contact(models.Model):
    name = models.CharField(max_length=120, verbose_name="Full Name")
    email = models.EmailField(validators=[EmailValidator()])
    company = models.CharField(max_length=120, blank=True, verbose_name="Company/Brand")
    message = models.TextField(blank=True, verbose_name="Campaign Details")
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact Submission"
        verbose_name_plural = "Contact Submissions"

    def _str_(self):
        return f"{self.name} - {self.email} - {self.created_at.strftime('%Y-%m-%d')}"


# Add this NewsletterSubscriber model
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-subscribed_at']

    def _str_(self):
        return self.email