from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
import json
import random
from .models import ProductCategory, Product
from basketapp.models import Basket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    context = {
        'page_title': 'главная',
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/index.html', context)


def main(request):
    title = 'Home'
    product = Product.objects.all()[:4]

    context = {
        'title': title,
        'product': product,
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


def get_menu():
    return ProductCategory.objects.filter(is_active=True)


def get_top_menu():
    return [
        {'href': 'main', 'name': 'HOME'},
        {'href': 'mainapp:products', 'name': 'PRODUCTS'},
        {'href': 'contact', 'name': 'CONTACT'}]

def get_hot_product():
    return random.choice(Product.objects.all())


def get_same_products(hot_product):
    return hot_product.category.product_set.exclude(pk=hot_product.pk)


# def product(request):
#     product = Product.objects.all()
#     hot_product = get_hot_product()
#
#     context = {
#         'page_title': 'каталог',
#         'product': product,
#         'top_menu': [
#             {'href': 'main', 'name': 'HOME'},
#             {'href': 'product:index', 'name': 'PRODUCTS'},
#             {'href': 'contact', 'name': 'CONTACT'}],
#         'basket': get_basket(request),
#         'hot_product': hot_product,
#         'same_products': get_same_products(hot_product),
#     }
#     return render(request, 'mainapp/products.html', context)


def products(request):
    products = Product.objects.all()
    hot_product = get_hot_product()

    context = {
        'page_title': 'каталог',
        'products': products,
        'top_menu': get_top_menu(),
        'catalog_menu': get_menu(),
        'basket': get_basket(request),
        'hot_product': hot_product,
        'same_products': get_same_products(hot_product),
    }
    return render(request, 'mainapp/products.html', context)


def product(request, pk):
    context = {
        'page_title': 'продукт',
        'product': get_object_or_404(Product, pk=pk),
        'top_menu': get_top_menu(),
        'basket': get_basket(request),
    }

    return render(request, 'mainapp/product.html', context)


def catalog(request, pk, page=1):
    if pk == '0':
        category = {
            'pk': 0,
            'name': 'все'
        }
        products = Product.objects.filter(is_active=True)
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.all()

    paginator = Paginator(products, 2)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context = {
        'title': 'каталог',
        'category': category,
        'products': products_paginator,
        'top_menu': get_top_menu(),
        'catalog_menu': get_menu(),
        'basket': get_basket(request),
    }

    return render(request, 'mainapp/products_list.html', context)


def contact(request):
    context = {
        'top_menu': get_top_menu(),
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
    return render(request, 'mainapp/product_details.html', context)
