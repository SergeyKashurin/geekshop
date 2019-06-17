from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
import json
import random
from .models import ProductCategory, Product
from basketapp.models import Basket


def main(request):
    title = 'Home'
    product = Product.objects.all()[:4]

    context = {
        'title': title,
        'product': product,
        'basket': Basket.objects.all(),
    }

    return render(request, 'mainapp/index.html', context)


def get_basket(request):
    if request.user.is_authenticated:
        return request.user.basket.all()
    else:
        return []


def get_basket_deleteme(request):
    if request.is_authenticated:
        return request.basket.all()
    else:
        return []


def get_hot_product():
    return random.choice(Product.objects.all())


def get_same_products(hot_product):
    return hot_product.category.product_set.exclude(pk=hot_product.pk)


def product(request):
    product = Product.objects.all()
    hot_product = get_hot_product()

    context = {
        'page_title': 'каталог',
        'product': product,
        'top_menu': [
            {'href': 'main', 'name': 'HOME'},
            {'href': 'product:index', 'name': 'PRODUCTS'},
            {'href': 'contact', 'name': 'CONTACT'}],
        'basket': get_basket(request),
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/product.html', context)


def contact(request):
    context = {
        'title': 'Contact Us',
        'top_menu': [
            {'href': 'main', 'name': 'HOME'},
            {'href': 'product:index', 'name': 'PRODUCTS'},
            {'href': 'contact', 'name': 'CONTACT'}],
    }
    return render(request, 'mainapp/contact.html', context)


def product_details(request, pk=None):

    context = {
        'title': 'products',
        'top_menu': [
            {'href': 'main', 'name': 'HOME'},
            {'href': 'product:index', 'name': 'PRODUCTS'},
            {'href': 'contact', 'name': 'CONTACT'}],
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket_deleteme(request.user),
    }
    return render(request, 'mainapp/product-details.html', context)
