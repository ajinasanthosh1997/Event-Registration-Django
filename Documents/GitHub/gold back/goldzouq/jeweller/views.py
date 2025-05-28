from django.views.generic import TemplateView,DetailView,ListView
from jeweller.models import JewellerProduct,Jeweler,JewellerCategory

class IndexView(ListView):
    model = Jeweler
    template_name = 'jeweler/index.html'
    context_object_name = 'jewelers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JewellerCategory.objects.all()
        context['products'] = JewellerProduct.objects.all()
        return context
    
class ProductListView(ListView):
    model = JewellerProduct
    template_name = 'jeweler/product.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = JewellerCategory.objects.all()  # Fetch all categories
        return context

    def get_queryset(self):
        return JewellerProduct.objects.all()
    
class ProductDetailView(DetailView):
    model = JewellerProduct
    template_name = 'jeweler/product-details.html'
    context_object_name = 'product'  