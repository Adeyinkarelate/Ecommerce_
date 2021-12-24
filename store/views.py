from django.shortcuts import render,get_object_or_404
from .models import Product
from category.models import Category 
from cart.views import _cart_id
from cart.models import CartItem
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q

# accepting the slug inside the view 
 # the slug , is slug from the model
def store(request,category_slug=None):
    categories = None 
    products = None 

    if category_slug != None:
        categories = get_object_or_404(Category,slug=category_slug) 
        products   = Product.objects.all().filter(category=categories,is_available=True )
        paginator = Paginator(products,6)
        page = request.GET.get('page') 
        page_product = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id') 
        paginator = Paginator(products,6)
        page = request.GET.get('page') 
        page_product = paginator.get_page(page)
        product_count = products.count()
        # instead of passing the product, we pass the 6 products
    context={
        'products':page_product ,
        'product_count':product_count
    }
    return render(request,'store/store.html' ,context)

def product_detail(request,category_slug,product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request) , product=single_product).exists()
    except Exception as e:
        raise e
    context ={
        'single_product':single_product,
        'in_cart':in_cart,
    }
    return render(request,'store/product_detail.html',context)






    # category wass goten from the product model and the slug should be gotten from the category model

# description__icontains=keyword : search through the whole description if you find anything relate to the keywords
# bring the product and show it inside the search results page

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('created_date').filter(Q(description__icontains=keyword )| Q(product_name__icontains=keyword))
            product_count = products.count()
    context = {
        'products' :products,
        'product_count':product_count,
    }
    return render(request,'store/store.html' , context)