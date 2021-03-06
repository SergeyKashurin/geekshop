from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import ProductCategory, Product
import random
from django.conf import settings
from django.core.cache import cache
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.views.decorators.cache import never_cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = 'category_{}'.format(pk)
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = 'product_{}'.format(pk)
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = 'products_in_category_orederd_by_price_{}'.format(pk)
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')


def index(request):
    context = {
        'page_title': 'главная',
        'basket': get_basket(request),
    }
    return render(request, 'mainapp/index.html', context)


def main(request):
    title = 'главная'
    products = get_products()[:3]

    context = {
        'title': title,
        'product': products,
    }
    return render(request, 'mainapp/index.html', context)


def get_basket(request):
    if request.user.is_authenticated:
        return request.user.basket.all().select_related()
    else:
        return []


def get_basket_deleteme(request):
    if request.is_authenticated:
        return request.basket.all().select_related()
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
    products = get_products()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    return hot_product.category.product_set.exclude(pk=hot_product.pk)


@never_cache
def products(request, pk=None, page=1):
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)

    if pk:
        if pk == '0':
            category = {
                'pk': 0,
                'name': 'все'
            }
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)

        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }

        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {
        'title': title,
        'links_menu': links_menu,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products.html', content)


@never_cache
def product(request, pk):
    title = 'продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)

    product = get_object_or_404(Product, pk=pk)

    content = {
        'title': title,
        'links_menu': links_menu,
        'product': product,
    }
    return render(request, 'mainapp/product.html', content)


def catalog(request, pk, page=1):
    if pk == '0':
        category = {
            'pk': 0,
            'name': 'все'
        }
        products = Product.objects.filter(is_active=True)
    else:
        category = get_object_or_404(ProductCategory, pk=pk)
        products = category.product_set.all().select_related()

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
        'links_menu': ProductCategory.objects.all().select_related(),
        'product': get_object_or_404(Product, pk=pk),
        'basket': get_basket_deleteme(request.user),
    }
    return render(request, 'mainapp/product_details.html', context)


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()

        if pk:
            if pk == '0':
                category = {
                    'pk': 0,
                    'name': 'все'
                }
                products = get_products_orederd_by_price()
            else:
                category = get_category(pk)
                products = get_products_in_category_orederd_by_price(pk)

            paginator = Paginator(products, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)

            content = {
                'links_menu': links_menu,
                'category': category,
                'products': products_paginator,
            }

            result = render_to_string(
                         'mainapp/includes/inc_products_list_content.html',
                         context=content,
                         request=request)

            return JsonResponse({'result': result})
