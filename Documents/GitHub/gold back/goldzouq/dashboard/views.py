from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView ,TemplateView,UpdateView,DeleteView
from main.models import *
from main.models import Testimonial
from .forms import *
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from jeweller.forms import *
from jeweller.models import *
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginView):
    template_name = 'dashboard/login.html'
    authentication_form = CustomLoginForm
        

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get the current user
        user = self.request.user
        
        if user.is_superuser:
            # If the user is a superuser, get all jewellers and their products
            context['jewelers'] = Jeweller.objects.all()
            context['products'] = JewellerProduct.objects.all()
        else:
            # Fetch the Jeweller instance using the user's email
            jeweller = get_object_or_404(Jeweller, email=user.email)
            
            # Filter products based on the Jeweller instance
            context['products'] = JewellerProduct.objects.filter(jeweller=jeweller)
        
        return context
    
class ProductListView(ListView):
    model = Product
    template_name = 'dashboard/product-list.html'
    context_object_name = 'products'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        
        # Create dictionaries to hold the forms for each product
        product_forms = {}
        specs_forms = {}
        description_forms = {}

        # Get all related objects in a single query
        product_ids = list(products.values_list('pk', flat=True))
        
        # Use `in` to fetch all specs and descriptions in one go
        specs_dict = ProductSpecs.objects.filter(product_id__in=product_ids).values('product_id', 'pk')
        description_dict = ProductDescription.objects.filter(product_id__in=product_ids).values('product_id', 'pk')
        
        # Convert lists of dicts to dictionaries with product_id as the key
        specs_map = {spec['product_id']: spec['pk'] for spec in specs_dict}
        description_map = {desc['product_id']: desc['pk'] for desc in description_dict}

        for product in products:
            # Create a form instance for each product
            product_forms[product.pk] = ProductForm(instance=product)
            
            # Handle ProductSpecs form
            specs_pk = specs_map.get(product.pk)
            if specs_pk:
                specs_instance = ProductSpecs.objects.get(pk=specs_pk)
                specs_forms[product.pk] = ProductSpecsForm(instance=specs_instance)
            else:
                specs_forms[product.pk] = ProductSpecsForm()

            # Handle ProductDescription form
            description_pk = description_map.get(product.pk)
            if description_pk:
                description_instance = ProductDescription.objects.get(pk=description_pk)
                description_forms[product.pk] = ProductDescriptionForm(instance=description_instance)
            else:
                description_forms[product.pk] = ProductDescriptionForm()

        # Add forms to context
        context['product_forms'] = product_forms
        context['specs_forms'] = specs_forms
        context['description_forms'] = description_forms

        return context

  
class CategoryListView(ListView):
    model = Category
    template_name = 'dashboard/category.html'
    context_object_name = 'categories'
    paginate_by = 5


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/categoryadd.html'
    success_url = reverse_lazy('dashboard:category_list')

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=slug)

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'dashboard/categoryadd.html'
    success_url = reverse_lazy('dashboard:category_list')

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=slug)

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('dashboard:category_list')

    def get_object(self):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Category, slug=slug)
  

class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'dashboard/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 5

class TestimonialCreateView(CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'dashboard/testimonial_form.html'
    success_url = reverse_lazy('dashboard:testimonial_list')

class TestimonialUpdateView(UpdateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'dashboard/testimonial_form.html'
    success_url = reverse_lazy('dashboard:testimonial_list')

class JewellerListView(ListView):
    model = Jeweller
    template_name = 'dashboard/jeweller_list.html'
    context_object_name = 'jewellers'
    paginate_by = 5


class JewellerCreateView(CreateView):
    model = Jeweller
    form_class = JewellerForm
    template_name = 'dashboard/jeweller_form.html'
    success_url = reverse_lazy('dashboard:jeweller_list')

class JewellerUpdateView(UpdateView):
    model = Jeweller
    form_class = JewellerForm
    template_name = 'dashboard/jeweller_form.html'
    success_url = reverse_lazy('dashboard:jeweller_list')

class JewellerDeleteView(DeleteView):
    model = Jeweller
    template_name = 'dashboard/jeweller_confirm_delete.html'
    success_url = reverse_lazy('dashboard:jeweller_list')

class JewelleryListView(ListView):
    model = Jeweler
    template_name = 'dashboard/jewellery_list.html'
    context_object_name = 'jewellers'
    paginate_by = 5

class JewelleryCreateView(CreateView):
    model = Jeweler
    form_class = JewelleryForm
    template_name = 'dashboard/jewellery_form.html'
    success_url = reverse_lazy('dashboard:jewellery_list')

class JewelleryUpdateView(UpdateView):
    model = Jeweler
    form_class = JewelleryForm
    template_name = 'dashboard/jewellery_form.html'
    success_url = reverse_lazy('dashboard:jewellery_list')

class JewellerDeleteView(DeleteView):
    model = Jeweler
    template_name = 'dashboard/jewellery_confirm_delete.html'
    success_url = reverse_lazy('dashboard:jewellery_list')


class JewellerCategoryListView(ListView):
    model = JewellerCategory
    template_name = 'dashboard/jeweller_category_list.html'
    context_object_name = 'categories'
    paginate_by = 5

class JewellerCategoryCreateView(CreateView):
    model = JewellerCategory
    form_class = JewellerCategoryForm
    template_name = 'dashboard/jeweller_category_form.html'
    success_url = reverse_lazy('dashboard:jeweller_category_list')

class JewellerCategoryUpdateView(UpdateView):
    model = JewellerCategory
    form_class = JewellerCategoryForm
    template_name = 'dashboard/jeweller_category_form.html'
    success_url = reverse_lazy('dashboard:jeweller_category_list')


class JewellerProductListView(ListView):
    model = JewellerProduct
    template_name = 'dashboard/jeweller_product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jewellers'] = Jeweler.objects.all()
        return context

class JewellerProductCreateView(CreateView):
    model = JewellerProduct
    form_class = JewellerProductForm
    template_name = 'dashboard/jeweller_product_form.html'
    success_url = reverse_lazy('dashboard:jeweller_product_list')

class JewellerProductUpdateView(UpdateView):
    model = JewellerProduct
    form_class = JewellerProductForm
    template_name = 'dashboard/jeweller_product_form.html'
    success_url = reverse_lazy('dashboard:jeweller_product_list')

# class JewellerCategoryDeleteView(DeleteView):
#     model = Category
#     template_name = 'dashboard/jeweller_category_confirm_delete.html'
#     success_url = reverse_lazy('dashboard:jeweller_category_list')

# def update_product(request):
#     if request.method == 'POST':
#         product_id = request.POST.get('product_id')
#         product = get_object_or_404(Product, pk=product_id)
        
#         # Handle ProductSpecs and ProductDescription forms
#         specs = get_object_or_404(ProductSpecs, product=product)
#         description = get_object_or_404(ProductDescription, product=product)

#         product_form = ProductForm(request.POST, request.FILES, instance=product)
#         specs_form = ProductSpecsForm(request.POST, instance=specs)
#         description_form = ProductDescriptionForm(request.POST, instance=description)

#         if product_form.is_valid() and specs_form.is_valid() and description_form.is_valid():
#             product_form.save()
#             specs_form.save()
#             description_form.save()

#             return redirect('dashboard:productlist')
#         else:
#             context = {
#                 'product_form': product_form,
#                 'specs_form': specs_form,
#                 'description_form': description_form,
#                 'product': product
#             }
#             return render(request, 'dashboard/edit_product.html', context)
#     else:
#         return JsonResponse({'error': 'Invalid request.'}, status=400)


def product_form_view(request, slug=None):
    if slug:
        # Editing an existing product
        product = get_object_or_404(Product, slug=slug)
        specs = get_object_or_404(ProductSpecs, product=product)
        description = get_object_or_404(ProductDescription, product=product)
        product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
        specs_form = ProductSpecsForm(request.POST or None, instance=specs)
        description_form = ProductDescriptionForm(request.POST or None, instance=description)
    else:
        # Adding a new product
        product_form = ProductForm(request.POST or None, request.FILES or None)
        specs_form = ProductSpecsForm(request.POST or None)
        description_form = ProductDescriptionForm(request.POST or None)

    if request.method == 'POST':
        if product_form.is_valid() and specs_form.is_valid() and description_form.is_valid():
            product = product_form.save()
            specs = specs_form.save(commit=False)
            specs.product = product
            specs.save()
            description = description_form.save(commit=False)
            description.product = product
            description.save()
            return redirect('dashboard:productlist')
        else:
            print("Product Form Errors:", product_form.errors)
            print("Specs Form Errors:", specs_form.errors)
            print("Description Form Errors:", description_form.errors)

    context = {
        'product_form': product_form,
        'specs_form': specs_form,
        'description_form': description_form,
        'categories': Category.objects.all(),
        'jewellers': Jeweller.objects.all(),
    }

    return render(request, 'dashboard/productadd.html', context)
  
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_form.html'
    success_url = reverse_lazy('productlist')
    

def logout_view(request):
    logout(request)
    # Redirect to a desired URL after logout
    return redirect('dashboard:login')  # Replace 'home' with your desired URL

def product_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'dashboard/productview.html', {'product': product})

def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('dashboard:productlist')
    return render(request, 'dashboard/product-list.html', {'product': product})

def add_or_edit_product(request, pk=None):
    if pk:
        # Editing an existing product
        product = get_object_or_404(Product, pk=pk)
        specs = get_object_or_404(ProductSpecs, product=product)
        description = get_object_or_404(ProductDescription, product=product)
        product_form = ProductForm(request.POST or None, request.FILES or None, instance=product)
        specs_form = ProductSpecsForm(request.POST or None, instance=specs)
        description_form = ProductDescriptionForm(request.POST or None, instance=description)
    else:
        # Adding a new product
        product_form = ProductForm(request.POST or None, request.FILES or None)
        specs_form = ProductSpecsForm(request.POST or None)
        description_form = ProductDescriptionForm(request.POST or None)

    if request.method == 'POST':
        if product_form.is_valid() and specs_form.is_valid() and description_form.is_valid():
            product = product_form.save()
            if pk:  # If editing, save existing specs and description
                specs = specs_form.save(commit=False)
                specs.product = product
                specs.save()
                description = description_form.save(commit=False)
                description.product = product
                description.save()
            else:  # If adding, save new specs and description
                specs = specs_form.save(commit=False)
                specs.product = product
                specs.save()
                description = description_form.save(commit=False)
                description.product = product
                description.save()
            return redirect('dashboard:productlist')
        else:
            print("Product Form Errors:", product_form.errors)
            print("Specs Form Errors:", specs_form.errors)
            print("Description Form Errors:", description_form.errors)

    context = {
        'product_form': product_form,
        'specs_form': specs_form,
        'description_form': description_form,
        'categories': Category.objects.all(),
        'jewellers': Jeweller.objects.all(),
    }

    return render(request, 'dashboard/productadd.html', context)

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard:home')  # Replace 'dashboard:home' with the name of your dashboard URL
            else:
                return render(request, 'dashboard/login.html', {'form': form, 'error': 'Invalid username or password.'})
        else:
            return render(request, 'dashboard/login.html', {'form': form, 'error': 'Invalid username or password.'})
    else:
        form = AuthenticationForm()
        return render(request, 'dashboard/login.html', {'form': form})