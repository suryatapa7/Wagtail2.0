from django.db import models
from django.forms import ValidationError
from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel,MultiFieldPanel,InlinePanel,PageChooserPanel,FieldRowPanel,HelpPanel,MultipleChooserPanel,TitleFieldPanel
from wagtail.fields import RichTextField
from wagtail.images import get_image_model
from wagtail.documents import get_document_model
from modelcluster.fields import ParentalKey




class HomePageOrderable(Orderable):
    page = ParentalKey(
        'home.HomePage',
        related_name='gallery_images',
        on_delete=models.CASCADE,
    )
    image = models.ForeignKey(
       get_image_model(), # get_image_model() returns the string 'wagtailimages.Image'
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="+",
    )


class HomePage(Page):
    template = "home/home_page.html"
    max_count = 1

    subtitle = models.CharField(max_length=100, blank=True, null=True)
    body = RichTextField(blank=True)

    image = models.ForeignKey(
       get_image_model(), # get_image_model() returns the string 'wagtailimages.Image'
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    custom_document = models.ForeignKey(
        get_document_model(), # get_document_model() returns the string 'wagtaildocs.Document'
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    cta_url = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    cta_external_url = models.URLField(
        blank=True,
        null=True
    )

    content_panels = Page.content_panels + [
        # TitleFieldPanel(
        #    'subtitle',
        #     help_text="The subtitle will appear below the title", 
        #     placeholder="Enter your subtitle"
        # ),
        # HelpPanel(
        #     content="<strong>HelpPanel<strong><p>Help text goes here</p>",
        #     heading="Note:"
        # ),
        # PageChooserPanel(
        #     'cta_url',
        #     'blogpages.BlogDetail',
        #     help_text="Select the appropriate blog page",
        #     heading = "Blog Page Selection"
        # )
        # FieldRowPanel(
        #     [    
        #         PageChooserPanel(
        #            'cta_url',
        #            'blogpages.BlogDetail',
        #             help_text="Select the appropriate blog page",
        #             heading = "Blog Page Selection",
        #             classname = "col6"
        #         ),
        #         FieldPanel(
        #             'cta_external_url',
        #             help_text="Enter an external URL for the call to action",
        #             heading="External URL",
        #             classname = "col6"
        #         ),  
        #     ],
        #     help_text="Select a page or enter a url",
        #     heading="Call to Action (CTA) URL"
        # ),

        MultiFieldPanel(
            [   
                HelpPanel(
                    content="<strong>HelpPanel<strong><p>Help text goes here</p>",
                    heading="Note:"
                ),
                FieldPanel('subtitle'),
                FieldRowPanel(
                    [    
                        PageChooserPanel(
                        'cta_url',
                        'blogpages.BlogDetail',
                            help_text="Select the appropriate blog page",
                            heading = "Blog Page Selection",
                            classname = "col6"
                        ),
                        FieldPanel(
                            'cta_external_url',
                            help_text="Enter an external URL for the call to action",
                            heading="External URL",
                            classname = "col6"
                        ),  
                    ],
                    help_text="Select a page or enter a url",
                    heading="Call to Action (CTA) URL"
                ),

            ],
            heading="MultiFieldPanel Demo",
            help_text="Random help text",
            classname="collapsed"
        ),
        # InlinePanel(
        #     'gallery_images',
        #     label="Gallery Images",
        #     min_num=2,
        #     max_num=4
        # )
        MultipleChooserPanel(
            'gallery_images',
            label="Gallery Images",
            min_num=2,
            max_num=4,
            chooser_field_name='image',
        )










        # FieldPanel("subtitle", read_only=True),
        # FieldPanel("cta_url"),
        # FieldPanel("cta_external_url"),
        # FieldPanel("body"),
        # FieldPanel("image"),
        # FieldPanel("custom_document"),
    ]

    def get_cta_url(self):
        if self.cta_url:
            return self.cta_url.url
        elif self.cta_external_url:
            return self.cta_external_url
        else:
            return None
    
    def clean(self):
        super().clean()
        if self.cta_url and self.cta_external_url:
            raise ValidationError({
                'cta_url': 'You can only have one CTA URL',
                'cta_external_url': 'You can only have one CTA URL',
            })


        