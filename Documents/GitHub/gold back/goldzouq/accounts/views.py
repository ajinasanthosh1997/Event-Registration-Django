from django.shortcuts import render, redirect
from .forms import PhoneLoginForm, OTPForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth import login
from django.core.cache import cache  # Import Django cache
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from twilio.rest import Client
import random
from .forms import *
from decouple import config
from main.models import *

User = get_user_model()

# Twilio setup
TWILIO_ACCOUNT_SID = config('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = config('TWILIO_AUTH_TOKEN')
TWILIO_VERIFY_SERVICE_SID = config('TWILIO_VERIFY_SERVICE_SID')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_otp_phone(phone_number, otp):
    print(otp)
    pass
    # client.verify.v2.services(TWILIO_VERIFY_SERVICE_SID).verifications.create(
    #     to=phone_number,
    #     channel="sms"
    # )

def login_with_otp(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

   
    phone_not_registered = False
    phone_form = PhoneLoginForm()

    if request.method == 'POST':
        phone_form = PhoneLoginForm(request.POST)
        if phone_form.is_valid():
            phone_number = phone_form.cleaned_data['phone_number']
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                phone_not_registered = True
            except User.MultipleObjectsReturned:
                pass
            else:
                otp = random.randint(100000, 999999)
                user.otp = str(otp)
                user.save()
                send_otp_phone(phone_number, otp)

                return redirect('accounts:phone_otp', phone_number=phone_number)

    return render(request, 'accounts/login_with_otp.html', {'phone_not_registered': phone_not_registered,
                                                            'phone_form': phone_form,
                                                            'testimonials': testimonials,
                                                            'parent_categories':parent_categories,
                                                            'women_products': women_products,
                                                            'men_products': men_products,
                                                            'kids_products': kids_products,
                                                            'newborn_products': newborn_products,})

def phone_otp(request, phone_number):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    if request.method == 'POST':
        otp_form = OTPForm(request.POST)
        if otp_form.is_valid():
            entered_otp = otp_form.cleaned_data['otp']
            try:
                user = User.objects.get(phone_number=phone_number)
                stored_otp = user.otp
                if stored_otp == entered_otp:
                    login(request, user)
                    return redirect('accounts:account')
                else:
                    messages.error(request, 'Incorrect OTP. Please try again.')
            except User.DoesNotExist:
                messages.error(request, 'User not found.')
        else:
            messages.error(request, 'Invalid OTP format.')
    else:
        otp_form = OTPForm()

    return render(request, 'accounts/phone_otp.html', {'phone_number': phone_number, 'otp_form': otp_form,'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,})

@login_required
def account(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('accounts:account')
        else:
            messages.error(request, 'Error updating profile. Please check the form.')
    else:  # For GET requests
        form = UserProfileForm(instance=user)
    context = {'user': user, 'form': form,
               'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,}
    return render(request, 'accounts/account.html', context)

def register(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

   
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print("########")
            form.save()
            # Redirect to a success page or login page
            return redirect('accounts:login_with_mail')
        else:
            print(form.errors)
    else:
        form = RegistrationForm()
    return render(request,'accounts/register.html', {'form': form,
                                                     'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,})

def signout(request):
    logout(request)
    return redirect('accounts:login_with_mail')

def otp_expired_page(request):
    return render(request, 'accounts/otp_expired.html')

def send_otp(email, otp):
    subject = 'Your OTP for Login'
    message = f'Your OTP for login is: {otp}'
    from_email = 'ajina@gmail.com'  # Update with your email
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

def login_with_mail(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

    
    email_not_registered = False
    email_form = EmailLoginForm()

    if request.method == 'POST':
        email_form = EmailLoginForm(request.POST)
        if email_form.is_valid():
            email = email_form.cleaned_data['email']
            # Check if the email exists in the database
            try:
                user = get_user_model().objects.get(email=email)
            except get_user_model().DoesNotExist:
                email_not_registered = True
            except get_user_model().MultipleObjectsReturned:
                pass
            else:
                # If the email exists, generate and send OTP
                otp = random.randint(100000, 999999)
                user.otp = str(otp)  # Assuming you have an 'otp' field in your User model
                user.save()  # Save the user instance after setting the OTP

                # Send OTP to the user's email
                send_otp(email, otp)

                # Redirect to a page where the user can enter the OTP
                return redirect('accounts:mail_otp', email=email)
    
    return render(request, 'accounts/login_with_mail.html', {'email_not_registered': email_not_registered, 'email_form': email_form,
                                                             'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,})

def verify_otp(email, entered_otp):
    try:
        # Retrieve the user from the database
        user = get_user_model().objects.get(email=email)
        
        # Retrieve the stored OTP from the user model
        stored_otp = user.otp

        print(f"Email: {email}, Entered OTP: {entered_otp}, Stored OTP: {stored_otp}")

        # Check if stored OTP matches the entered OTP
        if stored_otp == entered_otp:
            return True
        else:
            print("Incorrect OTP")
            return False
    except get_user_model().DoesNotExist:
        print("User not found")
        return False
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return False
    
def mail_otp(request, email):
    parent_categories = Category.objects.filter(parent__isnull=True)
    testimonials = Testimonial.objects.all()
    women_products = Product.objects.filter(gender='women')
    men_products = Product.objects.filter(gender='men')
    kids_products = Product.objects.filter(gender='kids')
    newborn_products = Product.objects.filter(gender='newborn')

   
    if request.method == 'POST':
        # If the form is submitted with the entered OTP
        entered_otp = request.POST.get('otp', '')
        
        # Verify the entered OTP
        if verify_otp(email, entered_otp):
            # Clear the OTP from the cache after successful verification
            cache_key = f"otp_{email}"
            cache.delete(cache_key)

            # Log in the user
            user = get_user_model().objects.get(email=email)
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

            messages.success(request, 'OTP verified successfully.')
            return redirect('accounts:account')
        else:
            messages.error(request, 'Incorrect OTP. Please try again.')

    # If it's a GET request or OTP verification failed, render the OTP entry page
    return render(request, 'accounts/mail_otp.html', {'email': email,
                                                      'testimonials': testimonials,
        'parent_categories':parent_categories,
        'women_products': women_products,
        'men_products': men_products,
        'kids_products': kids_products,
        'newborn_products': newborn_products,})
