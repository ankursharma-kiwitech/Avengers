from email.message import EmailMessage
from Tools.scripts import generate_token
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

from django.core.mail import EmailMessage, send_mail
from django.shortcuts import render, redirect

from django.template.loader import render_to_string
from Avengers.tokens import generate_token
from ProjectAvengers import settings
from django.views import View


# Create your views here.


def home (self):
    return render(self, "Avengers/index.html")


class register(View):

    def get (self, request):
        return render(request, "Avengers/signup.html")

    def post (self, request):
        if request.method == 'POST':
            # get values from user
            username = request.POST.get('username')
            pass1 = request.POST.get('pass1')
            pass2 = request.POST.get('pass2')
            email = request.POST.get('email')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')

            if User.objects.filter(username=username):
                messages.error(request, "Username already exist! Please try some other username.")
                return redirect('home')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Registered!!")
                return redirect('home')

            if len(username) > 20:
                messages.error(request, "Username must be under 20 characters!!")
                return redirect('home')

            if pass1 != pass2:
                messages.error(request, "Passwords didn't matched!!")
                return redirect('home')

            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!!")
                return redirect('home')

            myuser = User.objects.create_user(username=username, password=pass1, email=email)
            # myuser.first_name = firstname
            # myuser.last_name = lastname

            myuser.is_active = False

            myuser.save()

            messages.success(request,
                             "Your Account has been created successfully!! Please check your email to confirm your "
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

                'name': myuser,
                'domain': current_site.domain,
                'uid': myuser.pk,
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

            return redirect('login')

        else:
            messages.error(request, "Invalid Request!!")

        return redirect('home')


class Login(View):
    def get (self, request):
        return render(request, 'login.html')

    def post (self, request):
        if request.method == 'POST':
            username = request.POST.get('username')
            pass1 = request.POST.get('pass1')

            user = authenticate(username=username, password=pass1)

            if user is not None:
                login(request, user)
                messages.success(request, 'welcome Avenger  you are logged in Successful')
                return redirect('home')


            else:
                messages.error(request, 'Invalid Username or Password')
                return redirect('login')


class Logout(View):

    def get (self, request):
        return render(request, 'home.html')

    def post (self, request):
        if request.method == 'POST':
            logout(request)
            messages.success(request, 'Logout Successful')
            return redirect('home')
        logout(self)
        return redirect('home')


class Activate(View):
    def get (self, request, uid, token):

        try:
            uid = uid
            myuser = User.objects.get(pk=uid)


        except(TypeError, ValueError, OverflowError, myuser.DoesNotExist):
            myuser = None

        if myuser is not None:

            if token == token:
                myuser.is_active = True
                myuser.save()
                messages.success(request, "Your Account has been activated!!")
                return redirect('home')

        else:
            return render(request, 'activation_failed.html')

# def home (request):
#     return render(request, 'Avengers/home.html')
