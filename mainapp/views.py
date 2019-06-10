from django.shortcuts import render, get_object_or_404
import json
from .models import ProductCategory, Product
from basketapp.models import Basket

# Create your views here.


def main(request):
    title = 'Home'
    products = Product.objects.all()[:4]

    context = {'title': title, 'products': products}

    return render(request, 'mainapp/index.html', context)


def product(request, pk=None):
    print(pk)

    links_menu = ProductCategory.objects.all()
    title = 'Our Products Range'

    basket = []
    category = ''
    products = ''
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)

        if pk:
            if pk == '0':
                products = Product.objects.all().order_by('price')
                category = {'name': 'все'}
            else:
                category = get_object_or_404(ProductCategory, pk=pk)
                products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'product': products,
            'basket': basket,
        }

        return render(request, 'mainapp/products_list.html', context)

    same_products = Product.objects.all()[1:3]

    context = {
        'title': title,
        'links_menu': links_menu,
        'same_products': same_products
    }

    return render(request, 'mainapp/product.html', context)


def contact(request):
    content = {
        'title': 'Contact Us',
        'top__menu': [
            {'href': 'main', 'name': 'HOME'},
            {'href': 'product:index', 'name': 'PRODUCTS'},
            {'href': 'main', 'name': 'HISTORY'},
            {'href': 'test', 'name': 'TEST_JSON'},
            {'href': 'contact', 'name': 'CONTACT'}],
    }
    return render(request, 'mainapp/contact.html', content)


def test(request):
    json_data = open('mainapp/json/test.json')
    jsn = json.load(json_data)
    json_data.close()

    content = {
        'title': 'Test',
        'json': jsn,
        'top__menu': [
            {'href': 'main', 'name': 'HOME'},
            {'href': 'product:index', 'name': 'PRODUCTS'},
            {'href': 'main', 'name': 'HISTORY'},
            {'href': 'test', 'name': 'TEST_JSON'},
            {'href': 'contact', 'name': 'CONTACT'}],
    }
    return render(request, 'mainapp/test.html', content)
