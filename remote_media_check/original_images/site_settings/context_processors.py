from wagtail.models import Page, Locale

def navbar(request):
    print(request.LANGUAGE_CODE)
    locale = Locale.objects.get(language_code=request.LANGUAGE_CODE)
    return {
        "my_name": "Suryatapa Bhattacharya",
        "navbar_pages": Page.objects.live().in_menu().public().filter(locale=locale)
    }