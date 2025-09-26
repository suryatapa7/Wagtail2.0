#1. import stuff
#2. create a snippetviewset
#3. add some settings for that snippet viewset
#4. register the class as a snippet 

from wagtail.admin.panels import FieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from taggit.models import Tag
from blogpages.models import Author

@register_snippet
class TagSnippetViewSet(SnippetViewSet):
    model = Tag
    icon = "tag"
    add_to_admin_menu = True
    menu_label = "Tags"
    menu_order = 500
    list_display = ['name', 'slug']
    search_fields = ('name')
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

@register_snippet
class AuthorSnippet(SnippetViewSet):
    model = Author
    add_to_admin_menu = False
  
from django.core.cache import cache
from wagtail import hooks

@hooks.register('after_publish_page')
def delete_all_cache(request, page):
    cache.clear()
    # print("Page is", page)
    # print("Page id is:",page.id)
    # print("THIS IS RUNNING AFTER THE PAGE IS PUBLISHED")

from django.contrib.auth.models import Permission

@hooks.register('register_permissions')
def customer_permission_numero_uno():
    return Permission.objects.filter(
        content_type__app_label = 'blogpages',
        codename = 'add_author'
    )

from wagtail import hooks
from wagtail.admin.ui.components import Component
from django.utils.safestring import mark_safe

class WelcomePanel(Component):
    order = 10
    template_name = "panels/welcome_panel.html"
    # def render_html(self, request):
    #     return mark_safe("""
    #         <div style='background-color: #f1f1f1; padding: 20px; color: #333;' class='welcome-panel'>
    #             <h2 style='color: #333;'>Welcome to the Wagtail Admin!</h2>
    #             <p style='color: #333;'>We're glad to have you here.</p>
    #         </div>
    #     """)

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['request'] = parent_context['request']
        context['username'] = parent_context['request'].user.username
        context['message'] = "Welcome to the admin!"
        return context

    class Media:
        css = {
            'all': {'css/welcome_panel.css',}
        }

        js = (
            'js/welcome_panel.js',
        )
    
@hooks.register('construct_homepage_panels')
def any_function_name_here(request, panels):
    panels.append(WelcomePanel())

from wagtail.admin.site_summary import SummaryItem

class NewSummaryItem(SummaryItem):
    order = 200
    template_name = "panels/new_summary_item.html"

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['purchases'] = 1000
        return context
    
from wagtail.models import Page

class UnpublishedPages(SummaryItem):
    order = 400
    template_name = "panels/unpublished_pages.html"

    def get_context_data(self, parent_context):
        context = super().get_context_data(parent_context)
        context['total'] = Page.objects.all().filter(live=False).count()
        return context

@hooks.register('construct_homepage_summary_items')
def summary_items(request,items):
    items.append(
        NewSummaryItem(request)
    ) 

    items.append(
        UnpublishedPages(request)
    )