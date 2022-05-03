from email.message import EmailMessage
from Tools.scripts import generate_token
from debugpy.common.compat import force_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout

from django.core.mail import EmailMessage,send_mail
from django.http import HttpResponse
# from authentication.tokens import generate_token

# Create your views here.
from django.template.context_processors import request
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from ProjectAvengers import settings


def home(request):
    return render(request, "Avengers/index.html")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        confirm = request.POST.get('confirm')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        # mname = request.POST.get('middle name')
        lastname = request.POST.get('lastname')

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')

        if len(username) > 10:
            if pass1 != confirm:
                messages.error(request, "Passwords didn't matched!!")
                return redirect('home')

            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!!")
                return redirect('home')

            myuser = User.objects.create_user(username=username, password=pass1, email=email)
            myuser.first_name = firstname
            myuser.last_name = lastname

            myuser.is_active = False

            myuser.save()

            messages.success(request,
                             "Your Account has been created succesfully!! Please check your email to confirm your "
                             "email "
                             "address in order to activate your account.")

            # Welcome Email
            subject = "welcome to Avengers Tower!!"
            message = "Hello " + myuser.first_name + "!! \n" + "Welcome to Team Avengers!! \nThank you for visiting our " \
                                                               "website\n. We have also sent you a confirmation email, " \
                                                               "please confirm your email address. \n\nThanking " \
                                                               "You\nMarvel studio "
            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)

            # Email Address Confirmation Email
            current_site = get_current_site(request)
            email_subject = "Confirm your Email TO Login in Avengers tower!!"
            message2 = render_to_string('email_confirmation.html', {

                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser)
            })
            email = EmailMessage(
                email_subject,
                message2,
                settings.EMAIL_HOST_USER,
                [myuser.email],
            )
            email.fail_silently = True
            email.send()

            return redirect('signin')

        messages.error(request, "Username must be under 10 charcters!!")
        return redirect('home')

    return render(request, "Avengers/signup.html")




def signin(request):
    if request.method == 'POST':
        user = request.POST.get('username')
        pass1 = request.POST.get('pass1')

        username = authenticate(username=user, password=pass1)

        if user is not None:
            login(request, user)
            return redirect('home')
            firstname = user.firstname
            return render(request, "Avengers/index.html", {{'firstname': firstname}})

            messages.success(request, 'welcome Avenger  you are logged in Successful')

        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, "Avengers/login.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')


def activate (request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64), strings_only=True)
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, myuser.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.profile.signup_confirmation = True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('home')
    else:
        return render(request, 'activation_failed.html')

