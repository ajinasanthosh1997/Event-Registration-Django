
from django.urls import path
from . import views
from .views import ContactDetailListCreate,BlogListView,BlogDetailView,BlogsListView,RobotsTxtView

app_name = 'main'

urlpatterns = [
    path('',views.index,name='index'),
    path('about/',views.about,name='about'),
    path('work/',views.work,name='work'),
    path('contact/',views.contact,name='contact'),

    path('services/<slug:slug>/',views.service_details,name='service_details'),
    

    path('contact_details/', ContactDetailListCreate.as_view(), name='contact_detail_list_create'),
    path('customer_messages/', views.CustomerMessageListCreate.as_view(), name='customer_message_list_create'),

    path('team/', views.team, name='team'),

    path('blog/', BlogsListView.as_view(), name='blog'),
    path('blogs/',BlogListView.as_view(), name='blogs'),
    path('blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),


    path('gallery/', views.gallery_view, name='gallery'),

    path('robots.txt', RobotsTxtView.as_view(), name='robots_txt'),
    
]