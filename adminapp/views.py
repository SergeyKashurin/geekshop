from authapp.models import ShopUser
from django.shortcuts import get_object_or_404, render
from mainapp.models import Product, ProductCategory
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from authapp.forms import ShopUserRegisterForm
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.views.generic.detail import DetailView
from adminapp.forms import AdminShopUserCreateForm, AdminShopUserUpdateForm, AdminProductCategoryUpdateForm, AdminProductUpdateForm


class UsersListView(ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductCategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'


class ProductCategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'adminapp/category_update.html'
    success_url = reverse_lazy('admin:categories')
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'

        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'


class ProductCategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'adminapp/category_delete.html'
    success_url = reverse_lazy('admin:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductCategoryCreate(CreateView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:categories')
    fields = '__all__'


class ProductCategoryUpdate(UpdateView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:categories')
    form_class = AdminProductCategoryUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'категории/редактирование'
        return context


class ProductCategoryDelete(DeleteView):
    model = ProductCategory
    success_url = reverse_lazy('adminapp:categories')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class ProductDetail(DetailView):
    model = Product


@user_passes_test(lambda u: u.is_superuser)
def users(request):
    users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    context = {
        'title': 'админка/пользователи',
        'objects': users_list
    }
    return render(request, 'adminapp/users.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_create(request):
    if request.method == 'POST':
        form = AdminShopUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:index'))
    else:
        form = AdminShopUserCreateForm()

    context = {
        'title': 'пользователи/создание',
        'form': form
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_update(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)
    if request.method == 'POST':
        form = AdminShopUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:index'))
    else:
        form = AdminShopUserUpdateForm(instance=user)

    context = {
        'title': 'пользователи/редактирование',
        'form': form
    }
    return render(request, 'adminapp/user_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, pk):
    user = get_object_or_404(ShopUser, pk=pk)

    if request.method == 'POST':
        user.is_active = False
        user.save()
        return HttpResponseRedirect(reverse('adminapp:index'))

    context = {
        'title': 'пользователи/удаление',
        'user_to_delete': user
    }
    return render(request, 'adminapp/user_delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def categories(request):
    context = {
        'title': 'категории продуктов',
        'object_list': ProductCategory.objects.all()
    }
    return render(request, 'adminapp/productcategory_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def products(request, category_pk):
    cat_obj = get_object_or_404(ProductCategory, pk=category_pk)
    context = {
        'title': 'продукты',
        'category': cat_obj,
        'object_list': cat_obj.product_set.all()
    }
    return render(request, 'adminapp/product_list.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_read(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': 'продукт/подробнее',
        'object': product,
    }
    return render(request, 'adminapp/product_read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_create(request, category_pk):
    cat_obj = get_object_or_404(ProductCategory, pk=category_pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:products',
                                                kwargs={'category_pk': category_pk}))
    else:
        form = AdminProductUpdateForm(initial={'category': cat_obj})

    context = {
        'title': 'продукты/создание',
        'form': form,
        'category': cat_obj,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_update(request, pk):
    obj = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = AdminProductUpdateForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('adminapp:products',
                                                kwargs={'category_pk': obj.category.pk}))
    else:
        form = AdminProductUpdateForm(instance=obj)

    context = {
        'title': 'продукты/редактирование',
        'form': form,
        'category': obj.category,
    }
    return render(request, 'adminapp/product_update.html', context)


@user_passes_test(lambda u: u.is_superuser)
def product_delete(request, pk):
    obj = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        obj.is_active = False
        obj.save()
        return HttpResponseRedirect(reverse('adminapp:products', kwargs={'category_pk': obj.category.pk}))

    context = {
        'title': 'продукты/удаление',
        'obj_to_delete': obj,
    }
    return render(request, 'adminapp/product_delete.html', context)
