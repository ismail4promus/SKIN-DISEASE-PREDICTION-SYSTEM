from django.contrib.auth import tokens
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, login, authenticate
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from .models import CreateUser
import random

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def forgot(request):
    if request.method == 'POST':
        username = request.POST["email"]
        user = User.objects.filter(username=username)
        #print(user)
        if user :
            userdetails = User.objects.get(username=username)
            code = random.randint(100000,999999)
            details = CreateUser.objects.get(user_id=userdetails.id)
            details.userresetpassword = code
            details.save()
            subject = 'Reset Password Verification Code!'
            message = f'Hi {details.userfirstname},\nYour reset password verification code is: {code}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [username,]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            messages.success(request, "Verification code is successfully sent to your email!.")
            return redirect('/account/resetpassword/'+str(userdetails.id))
        else:
            messages.error(request, "Invalid email.")
            return redirect("/account/forgot")
    return render(request, 'forgot.html')

def resetpassword(request, id):
    if request.method == 'GET':
        return render(request, 'reset_password.html', {'id':id})
    else:
        pass1 = request.POST['password']
        pass2 = request.POST['cpassword']
        code = request.POST['verification_code']
        if pass1 == pass2:
            profile = CreateUser.objects.get(user_id=id)
            if(code == profile.userresetpassword):
                user_id = profile.user_id
                user = User.objects.get(id=user_id)
                user.set_password(pass1)
                user.save()
                messages.success(request, "Password changed successfully.")
                return redirect('/account/login')
            else:
                messages.error(request, "Verification code doesn't match.")
                return redirect('/account/resetpassword/' + str(id))
        else:
            messages.error(request, "Password doesn't match.")
            return redirect('/account/resetpassword/' + str(id))

def Login(request):
    if request.method == 'POST' :
        username = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None :
            # messages.success(request, "Login successfull.")
            login(request, user)
            details = CreateUser.objects.get(user=user)
            if details.user_role=='admin':
                return redirect('/adminarea')
            else:
                return redirect('/dashboard')
        else :
            messages.error(request, "Invalid email or password.")
            return redirect("/account/login")
    return render(request, 'login.html')

def Register(request):
    if request.method == 'POST' :
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        password = request.POST["password"]
        phone = request.POST["phone"]
        if User.objects.filter(username=email).exists() :
            messages.error(request, "This email already exists.")
            return redirect('/account/register')
        else :
            user = User.objects.create_user(username=email, password=password)
            user.is_active = False
            user.save()
            
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            create = CreateUser(user=user, userfirstname=fname, userlastname=lname, userphone=phone, userverification=token, user_role='subscriber')
            create.save()
            # login(request, user)
            subject = 'Registration to our site'
            message = f'Hi {fname},\nactivate your account at http://127.0.0.1:8000/account/activate/{uid}/{token}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email,]
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
            messages.success(request, "Registration successfull.")
            messages.info(request, "Please check your email to activate account.")
            return redirect('/account/login')
    return render(request, 'register.html')
    
def Activate(request, uidb64, token):
    UserModel = get_user_model()
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=UserModel._default_manager.get(pk=uid)
    except(TypeError,ValueError, OverflowError,User.DoesNotExist):
        user=None
    if user is not None :
        details = CreateUser.objects.get(user=user)
        if details.userverification==token :
            user.is_active=True
            user.save()
            messages.success(request," Your account is activated now, you can now log in")
            return redirect('/account/login')
        else :
            messages.warning(request, "activation link is invalid")
            return redirect('/account/register')
    else:
        messages.warning(request, "activation link is invalid")
        return redirect('/account/register')