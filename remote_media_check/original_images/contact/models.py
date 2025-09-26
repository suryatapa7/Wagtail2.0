from django.db import models
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from modelcluster.fields import ParentalKey

#  1. Imports
#  2. FormField(AbstractFormField)
#  3. Contact Page

class FormField(AbstractFormField):
    page  = ParentalKey(
        'ContactPage',
        on_delete = models.CASCADE,
        related_name= 'form_fields'
    )

class ContactPage(AbstractEmailForm):
    template = "contact/contact_page.html"
    body = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('body'),
        FieldPanel('thank_you_text'),
        InlinePanel('form_fields', label="Custom Form Fields"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ])
    ]