from django.core.exceptions import ValidationError
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.blocks import StructBlockValidationError,ListBlockValidationError



class TextBlock(blocks.TextBlock):
    def __init__(self, **kwargs):
        super().__init__(
        **kwargs,  
        help_text = "This is from my TextBlock(help text is here)",
        max_length=10,
        min_length=2,
        required=False,
    )
        
    def clean(self, value):
        value = super().clean(value)
        if "wordpress" in value.lower():
            raise ValidationError("The word 'wordpress' is not allowed in this block.")
        return value
        
    class Meta: 
        icon = "strikethrough"
        # label = "Text Block"
        template = "blocks/text_block.html"
        group="Standalone Blocks"
        

class InfoBlock(blocks.StaticBlock):
   
   class Meta:
       # icon="..."
       template="blocks/info_block.html"
       admin_text = "This is from my InfoBlock"
       label="General Information"
       group="Standalone Blocks"

# from wagtail.blocks import StructBlockValidationError

class FAQBlock(blocks.StructBlock):
    question = blocks.CharBlock()
    answer = blocks.RichTextBlock(
        features=['bold', 'italic',]
    )

    def clean(self, value):
        cleaned_data = super().clean(value)

        # Check "question"
        if 'wordpress' in cleaned_data['question'].lower():
            raise StructBlockValidationError(
                block_errors={
                    'question': ValidationError("The word 'wordpress' is not allowed in the question.")
                }
            )

        # Check "answer"
        if 'wordpress' in str(cleaned_data['answer']).lower():
            raise StructBlockValidationError(
                block_errors={
                    'answer': ValidationError("The word 'wordpress' is not allowed in the answer.")
                }
            )

        return cleaned_data


class FAQListBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super().__init__(FAQBlock(),**kwargs)
    
    def clean(self, value):
        cleaned_data = super().clean(value)
        errors = {}

        for index,obj in enumerate(cleaned_data):
            if 'wordpress' in str(obj['answer']).lower():
                errors[index] = ValidationError("The word 'wordpress' is not allowed in the answer.")

        if errors:
            raise ListBlockValidationError(
                block_errors=errors,
            )
        return cleaned_data

    class Meta:
        min_num = 1
        max_num = 5
        label = "Frequently Asked Questions"
        group = "Iterables"
        # icon = "..."
        template = "blocks/faq_list_block.html"

class CarouselBlock(blocks.StreamBlock):
    image = ImageChooserBlock()
    quotation = blocks.StructBlock(
        [
            ('text', blocks.TextBlock()),
            ('author', blocks.TextBlock()),
        ]
    )

    def clean(self, value):
        value = super().clean(value)
        images = [item for item in value if item.block_type == 'image']
        quotations = [item for item in value if item.block_type == 'quotation']

        if not images or not quotations:
            raise ValidationError("Carousel must contain at least one image and one quotation.")
        
        if len(images) != len(quotations):
            raise ValidationError("Carousel must contain the same number of images and quotations.")
        
        return value

    class Meta:
        template = "blocks/carousel_block.html"
        group = "Iterables"

class CallToAction1(blocks.StructBlock):
    text = blocks.RichTextBlock(
        features=['bold', 'italic',],
        required=True,
    )
    page = blocks.PageChooserBlock()
    button_text = blocks.CharBlock(
        max_length=100,
        required=False,
    )

    def get_context(self,value,parent_context=None):
        context = super().get_context(value, parent_context=parent_context)
        page = value.get('page')
        button_text = value.get('button_text')
        context['button_copy'] = button_text if button_text else f'Read: {page.title}'
        return context

    class Meta:
        label = 'CTA #1'
        template ="blocks/call_to_action_1.html"

class ImageBlock(ImageChooserBlock):

    def get_api_representation(self, value, context=None):
        return {
            'id': value.id,
            'title': value.title,
            'src': value.get_rendition('fill-400x400').url,
        }
    
    def get_context(self, value, parent_context=None):
        from blogpages.models import BlogDetail
        context = super().get_context(value, parent_context)
        context['blog_posts'] = BlogDetail.objects.all().live().public()
        return context


    class Meta:
        template = "blocks/image_block.html"
        group = "Standalone Blocks"


class CustomPageChooserBlock(blocks.PageChooserBlock):
    def get_api_representation(self, value, context=None):
        return {
            'id': value.id,
            'title': value.title,
            'subtitle': value.specific.subtitle,
            'url': value.url,
          
        }