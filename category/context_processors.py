from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)

# since we are using context process
# we must inform our templates
# appname.filename.functionname
# 'category.context_processors.menu_links',
# with this,the menu_links is now available to use in anyplace we want
