from django.shortcuts import render
import json
from .models import ProductCategory, Product

# Create your views here.


def main(request):
    title = 'Home'
    products = Product.objects.all()[:4]

    content = {'title': title, 'products': products}

    return render(request, 'mainapp/index.html', content)


def product(request, pk=None):
    print(pk)
    content = {
        'title': 'Our Products Range',
        'top__menu': [
            {'href': 'main', 'name': 'HOME'},
            {'href': 'product:index', 'name': 'PRODUCTS'},
            {'href': 'main', 'name': 'HISTORY'},
            {'href': 'test', 'name': 'TEST_JSON'},
            {'href': 'contact', 'name': 'CONTACT'}],
    }
    return render(request, 'mainapp/product.html', content)


def contact(request):
    content = {
        'title': 'Contact Us',
        'top__menu': [
            {'href': 'main', 'name': 'HOME'},
            {'href': 'product', 'name': 'PRODUCTS'},
            {'href': 'main', 'name': 'HISTORY'},
            {'href': 'test', 'name': 'TEST_JSON'},
            {'href': 'contact', 'name': 'CONTACT'}],
    }
    return render(request, 'mainapp/contact.html', content)


def test(request):
    json_data = open('static/test.json')
    jsn = json.load(json_data)
    json_data.close()

    content = {
        'title': 'Test',
        'json': jsn,
        'top__menu': [
            {'href': 'main', 'name': 'HOME'},
            {'href': 'product', 'name': 'PRODUCTS'},
            {'href': 'main', 'name': 'HISTORY'},
            {'href': 'test', 'name': 'TEST_JSON'},
            {'href': 'contact', 'name': 'CONTACT'}],
    }
    return render(request, 'mainapp/test.html', content)
