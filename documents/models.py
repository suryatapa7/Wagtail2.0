from django.db import models

from wagtail.documents.models import AbstractDocument,Document


# Create your models here.
class CustomDocument(AbstractDocument):
    description = models.CharField(max_length=255, blank=True)
    admin_form_fields = Document.admin_form_fields + ('description',)