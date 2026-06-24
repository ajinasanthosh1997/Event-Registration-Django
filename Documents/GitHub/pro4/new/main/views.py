from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from .models import *
from .serializers import *
from django.http import HttpResponseRedirect
from django.views.generic import ListView
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.core.mail import send_mail, EmailMessage
import logging
import smtplib
import socket
import traceback
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime

from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response

from .models import CustomerMessage
from .serializers import CustomerMessageSerializer

logger = logging.getLogger(__name__)

class CustomerMessageListCreate(generics.ListCreateAPIView):
    queryset = CustomerMessage.objects.all()
    serializer_class = CustomerMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        message = None
        email_failure = False
        try:
            # Save the message to database
            message = serializer.save()
            
            # Email content - simple plain text
            customer_subject = "Thank You for Contacting Pro4"
            customer_body = f"""Dear {message.name},

            Thank you for reaching out to us! We've received your message and our team will get back to you soon.

            Here are your message details:
            Email: {message.email}
            Message: {message.message}

            We typically respond within 24-48 hours. If you have urgent inquiries, feel free to call us at +973 3394 9648,+973 33861121.

            Best regards,
            The Pro4 Team


            Pro4 3.0 – Your Growth Engine
            Al  Seef , Bahrain
            """
                        
            admin_subject = f"New Message from {message.name}"
            admin_body = f"""New message received from contact form:

            Name: {message.name}
            Email: {message.email}
            Message:
            {message.message}

            Received at: {message.created_on.strftime('%Y-%m-%d %H:%M')}
            """
            
            # Try to send emails
            try:
                # Send customer confirmation
                customer_sent = self.send_email(
                    customer_subject, 
                    customer_body, 
                    message.email
                )
                
                # Send admin notification
                admin_sent = self.send_email(
                    admin_subject, 
                    admin_body, 
                    settings.ADMIN_EMAIL
                )
                
                # If either email failed
                if not customer_sent or not admin_sent:
                    email_failure = True
                    
            except Exception as e:
                email_failure = True
                logger.error(f"Email sending failed: {str(e)}")
                logger.error(traceback.format_exc())

            if not email_failure:
                return Response({
                    "success": True,
                    "message": "Your message has been sent successfully!",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    "success": True,
                    "message": "Message received! We'll contact you soon.",
                    "data": serializer.data,
                    "warning": "Email confirmation might not have been sent"
                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error processing contact form: {str(e)}")
            logger.error(traceback.format_exc())
            return Response({
                "success": False,
                "error": "An error occurred while processing your request"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def send_email(self, subject, body, recipient):
        """Send plain text email with deliverability best practices"""
        required_settings = {
            "BREVO_LOGIN": settings.BREVO_LOGIN,
            "BREVO_PASSWORD": settings.BREVO_PASSWORD,
            "BREVO_SENDER_EMAIL": settings.BREVO_SENDER_EMAIL,
        }
        missing_settings = [name for name, value in required_settings.items() if not value]
        if missing_settings:
            logger.warning(f"Email not sent. Missing settings: {', '.join(missing_settings)}")
            return False

        if not recipient:
            logger.warning("Email not sent. Missing recipient address.")
            return False

        try:
            # Create message with proper headers
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = formataddr(("Pro4 Team", settings.BREVO_SENDER_EMAIL))
            msg['To'] = recipient
            msg['Date'] = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S +0000')
            
            # Add headers to reduce spam classification
            msg['X-Priority'] = '3'  # Normal priority
            msg['Precedence'] = 'bulk'
            if hasattr(settings, 'UNSUBSCRIBE_EMAIL'):
                msg['List-Unsubscribe'] = f'<mailto:{settings.UNSUBSCRIBE_EMAIL}>'
            
            # Use configured Brevo SMTP server
            with smtplib.SMTP(settings.BREVO_SMTP_SERVER, settings.BREVO_SMTP_PORT, timeout=15) as server:
                server.ehlo()
                
                # Start TLS if available
                if server.has_extn('STARTTLS'):
                    server.starttls()
                    server.ehlo()
                
                server.login(settings.BREVO_LOGIN, settings.BREVO_PASSWORD)
                server.sendmail(settings.BREVO_SENDER_EMAIL, [recipient], msg.as_string())
            
            logger.info(f"Email sent to {recipient}")
            return True
                
        except (socket.gaierror, socket.timeout, ConnectionRefusedError) as e:
            logger.warning(f"Connection failed: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False

class BaseView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_items'] = NavbarItem.objects.all()
        return context


class ContactDetailListCreate(generics.ListCreateAPIView):
    queryset = ContactDetail.objects.all()
    serializer_class = ContactDetailSerializer



def index(request):
    featured_works = FeaturedWork.objects.select_related('work').order_by('order')[:5]
    navbar_items = NavbarItem.objects.all()
    is_home_page = True
    latest_video = HomePageVideo.objects.filter().order_by('-created_at').first()
    
    testimonials = Testimonial.objects.all()
    services = Service.objects.all().order_by('number')
    
    logo_group1 = Logo.objects.filter(carousel_group=1)
    logo_group2 = Logo.objects.filter(carousel_group=2)
    logo_group3 = Logo.objects.filter(carousel_group=3)
    # New addition: get screenshots marked for homepage
    homepage_screenshots = WorkScreenshot.objects.filter(show_on_home=True).order_by('order')
    
    context = {
        'method_steps': MethodStep.objects.all(),
        'featured_works': featured_works,
        'is_home_page': is_home_page,
        'testimonials': testimonials,
        'services': services,
        'latest_video': latest_video,
        'navbar_items': navbar_items,
        'logo_group1': logo_group1,
        'logo_group2': logo_group2,
        'logo_group3': logo_group3,
        'homepage_screenshots': homepage_screenshots,
    }
    return render(request, 'main/index.html', context)

def about(request):
    navbar_items = NavbarItem.objects.all()
    aboutcards=About.objects.all()
    
    logo_group1 = Logo.objects.filter(carousel_group=1)
    logo_group2 = Logo.objects.filter(carousel_group=2)
    logo_group3 = Logo.objects.filter(carousel_group=3)
    return render(request,'main/about.html',{'logo_group1': logo_group1,
        'logo_group2': logo_group2,
        'logo_group3': logo_group3,'aboutcards':aboutcards,'navbar_items':navbar_items})

def work(request):
    navbar_items = NavbarItem.objects.all()
    projectsdone = ProjectsDone.objects.latest('uploaded_at')
    projects = Project.objects.all().order_by('order')[:4]
    
    # Get selected division from query parameter
    division_slug = request.GET.get('division')
    divisions = Service.objects.all()
    
    if division_slug and division_slug != 'all':
        works = Work.objects.filter(division__slug=division_slug)
    else:
        works = Work.objects.all()
    
    return render(request, 'main/work.html', {
        'works': works,
        'projects': projects,
        'projectsdone': projectsdone,
        'navbar_items': navbar_items,
        'divisions': divisions
    })

def contact(request):
    navbar_items = NavbarItem.objects.all()
    testimonials = Testimonial.objects.all()
    faqs=FAQ.objects.all()
    context={'faqs':faqs,'testimonials': testimonials,'navbar_items':navbar_items}
    return render(request,'main/contact.html',context)

def service_details(request,slug):
    navbar_items = NavbarItem.objects.all()
    service = get_object_or_404(Service, slug=slug)
    subservices = SubService.objects.filter(service=service)
    testimonials = Testimonial.objects.all()
    return render(request,'main/services-detail.html',{'testimonials': testimonials,'service':service,'subservices':subservices,'navbar_items':navbar_items})

def service_details1(request):
    navbar_items = NavbarItem.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request,'main/service-details2.html',{'testimonials': testimonials,'navbar_items':navbar_items})

def service_details2(request):
    navbar_items = NavbarItem.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request,'main/service-details3.html',{'testimonials': testimonials,'navbar_items':navbar_items})

def service_details3(request):
    navbar_items = NavbarItem.objects.all()
    testimonials = Testimonial.objects.all()
    return render(request,'main/service-details4.html',{'testimonials': testimonials,'navbar_items':navbar_items})

def team(request):
    navbar_items = NavbarItem.objects.all()
    teams = TeamImage.objects.filter()[:1]
    ceo = CEO.objects.filter(is_ceo=True).first()  # Assuming there's only one main CEO
    other_ceos = CEO.objects.all()
    team_members = TeamMember.objects.all()
    return render(request, 'main/team.html', {'teams': teams,'ceo': ceo,
                                               'other_ceos': other_ceos,
                                                 'team_members': team_members,
                                                 'navbar_items':navbar_items})

class BlogsListView(ListView):
    model = Blog
    template_name = 'main/blog.html'
    context_object_name = 'blogs'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Queryset for featured blogs
        context['featured_blogs'] = Blog.objects.filter(is_featured=True)
        context['navbar_items'] = NavbarItem.objects.all()
        # Queryset for regular blogs
        context['blogs'] = Blog.objects.filter(is_featured=False).order_by('-date')[:4]
        return context
    

def story_list(request):
    navbar_items = NavbarItem.objects.all()
    stories = Story.objects.all().order_by('-date')
    paginator = Paginator(stories, 6)  # Show 9 stories per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'main/story_list.html', {'page_obj': page_obj,'navbar_items':navbar_items})



class BlogListView(ListView):
    model = Blog
    template_name = 'main/blogs.html'
    context_object_name = 'blogs'
    queryset = Blog.objects.order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_items'] = NavbarItem.objects.all()
        return context



class BlogDetailView(DetailView):
    model = Blog
    template_name = 'main/blog-detail.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['navbar_items'] = NavbarItem.objects.all()
        return context
    

def gallery_view(request):
    navbar_items = NavbarItem.objects.all()
    gallery_groups = GalleryGroup.objects.prefetch_related('images').all()
    return render(request, 'main/gallery.html', { 'gallery_groups': gallery_groups,'navbar_items':navbar_items})

def story_detail(request, slug):
    navbar_items = NavbarItem.objects.all()
    story = get_object_or_404(Story, slug=slug)
    return render(request, 'main/story_detail.html', {'story': story,'navbar_items':navbar_items})

class RobotsTxtView(TemplateView):
    template_name = 'main/robots.txt'
    content_type = 'text/plain'
