from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from .models import Category
from jeweller.models import Jeweler
from django.shortcuts import render, get_object_or_404

def get_child_categories(request, parent_id):
    child_categories = Category.objects.filter(parent_id=parent_id).values('id', 'name')
    return JsonResponse(list(child_categories), safe=False)

def index(request):
    products = Product.objects.all()
    logos = Jeweler.objects.all()
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    context = {
        'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,
        'logos':logos,
        'products':products,
        
    }
    return render(request,'main/index.html',context)

def calculator(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    context = {
        'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,
        
    }
    return render(request,'main/calculator.html',context)

def privacy_policy(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    context = {
        'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,
        
    }
    return render(request,'main/privacy_policy.html',context)

def product_list(request):
    # Get filter parameters from the request
    gender = request.GET.getlist('gender')
    jeweller = request.GET.getlist('jeweller')
    category = request.GET.get('category')
    gold_purity = request.GET.getlist('gold_purity')
    metal_color = request.GET.getlist('metal_color')

    # Start with all products
    products = Product.objects.all()

    # Apply filters based on the parameters received
    if gender:
        products = products.filter(gender__in=gender)
    if jeweller:
        products = products.filter(jeweller__in=jeweller)
    if category:
        products = products.filter(category=category)
    if gold_purity:
        products = products.filter(gold_purity__in=gold_purity)
    if metal_color:
        products = products.filter(metal_color__in=metal_color)

    # Fetch related data for the context
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()

    # Additional filtering for specific categories (if needed)
    women_products = products.filter(gender='women')
    men_products = products.filter(gender='men')
    kids_products = products.filter(gender='kids')
    newborn_products = products.filter(gender='newborn')

    # Prepare context for the template
    context = {
        'testimonials': testimonials,
        'parent_categories': parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,
        'products': products,
        'gender_choices': Product.GENDER_CHOICES,
        'jeweller_choices': ProductSpecs.JEWELLER_CHOICES,  # Assuming these are defined in your choices
        # 'category_choices': ProductSpecs.CATEGORY_CHOICES,
        'gold_purity_choices': Product.GOLD_PURITY_CHOICES,
        'metal_color_choices': Product.METAL_COLOR_CHOICES,
        'selected_genders': gender,
        'selected_jewellers': jeweller,
        'selected_category': category,
        'selected_gold_purity': gold_purity,
        'selected_metal_color': metal_color,
    }

    # Render the template with the context data
    return render(request, 'main/product-list.html', context)

def product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    specs = product.specs
    description = product.desc
    if product.gender:
        related_products = Product.objects.filter(gender=product.gender).exclude(id=product.id)[:6]
    else:
        related_products = Product.objects.none()
    
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    context = {
        'product': product,
        'specs': specs,
        'description': description,
        'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,
        'related_products': related_products,
    }
    return render(request,'main/product.html',context)

def reels(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    context = {
        'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,
        
    }
    return render(request,'main/reels.html',context)

def seller(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    context = {
        'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,
        
    }
    if request.method == 'POST':
        store_name = request.POST.get('store_name')
        contact_person_name = request.POST.get('contact_person_name')
        contact_number = request.POST.get('contact_number')
        website_or_instagram = request.POST.get('website_or_instagram')
        designation = request.POST.get('designation')
        email = request.POST.get('email')

        store = Store.objects.create(
            store_name=store_name,
            contact_person_name=contact_person_name,
            contact_number=contact_number,
            website_or_instagram=website_or_instagram,
            designation=designation,
            email=email
        )
        return redirect('main:seller')  # Redirect to admin index page after form submission
    return render(request,'main/seller.html',context)

def terms_and_conditions(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    context = {
        'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,
        
    }
    return render(request,'main/terms_and_conditions.html',context)




