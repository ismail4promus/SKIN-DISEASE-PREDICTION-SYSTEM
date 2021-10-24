from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from account.models import CreateUser
from django.contrib import messages
from diagnose.models import Disease
from diagnose.models import Diseasetype

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    if request.user.is_authenticated and request.user.is_staff==False:
        profile = CreateUser.objects.get(user=request.user)
        data = Disease.objects.filter(user=request.user)
        return render(request, 'dashboard.html', {'data':data,'profile':profile,})
    else :
        return redirect('/account/login')

def adminarea(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        profile = CreateUser.objects.filter(user_role='subscriber')
        current_user = CreateUser.objects.get(user=request.user)
        context = {
            'profile': profile
        }
        return render(request, 'adminarea.html', {'profile': profile,'cuser': current_user })
    else:
        return redirect('/account/login')
def userdetails(request, id):
    if request.user.is_authenticated and request.user.is_staff == True:
        profile = CreateUser.objects.get(user=request.user)
        userprofile = CreateUser.objects.get(user=id)
        data = Disease.objects.filter(user=id)
        return render(request, 'userdetails.html', {'data': data, 'profile': profile, 'userprofile': userprofile })
    else:
        return redirect('/account/login')

def editreport(request,id):
    if request.method == 'GET' :
        if request.user.is_authenticated and request.user.is_staff==True:
            disease_details = Diseasetype.objects.get(id=id)
            profile = CreateUser.objects.get(user=request.user)
            return render(request, 'editreport.html', {'data': disease_details, 'profile': profile, 'edit_id':id})
        else :
            return redirect('/account/login')
    elif request.method == 'POST' :
        name = request.POST['disease_name']
        description = request.POST['disease_description']
        if name == "":
            messages.error(request, "Please fill out disease name!")
            return redirect('/edit-report/'+str(id))
        elif description == "":
            messages.error(request, "Please fill out disease report!")
            return redirect('/edit-report/'+str(id))
        else :
            dtype = Diseasetype.objects.get(id=id)
            dtype.name = name
            dtype.description = description
            dtype.save()
            messages.success(request, "Report updated successfully.")
            return redirect('/edit-report/'+str(id))

def reports(request):
    if request.user.is_authenticated and request.user.is_staff == True:
        data = Diseasetype.objects.filter()
        profile = CreateUser.objects.get(user=request.user)
        return render(request, 'reports.html', {'data': data, 'profile':profile})
    else:
        return redirect('/account/login')

def details(request, id):
    if request.user.is_authenticated and request.user.is_staff==False:
        profile = CreateUser.objects.get(user=request.user)
        data = Disease.objects.filter(id=id)
        for d in data:
            disease_one = Diseasetype.objects.filter(name=d.summary)
            disease_two = Diseasetype.objects.filter(name=d.summary_inception)
            disease_three = Diseasetype.objects.filter(name=d.summary_vgg)

        return render(request, 'details.html', {'data':data,'profile':profile,'one':disease_one,'two':disease_two,'three':disease_three})

    elif request.user.is_authenticated and request.user.is_staff==True:
        profile = CreateUser.objects.get(user=request.user)
        data = Disease.objects.filter(id=id)
        for d in data:
            disease_one = Diseasetype.objects.filter(name=d.summary)
            disease_two = Diseasetype.objects.filter(name=d.summary_inception)
            disease_three = Diseasetype.objects.filter(name=d.summary_vgg)
            userprofile = CreateUser.objects.get(user=d.user_id)

        return render(request, 'details.html', {'data':data,'profile':profile,'userprofile':userprofile,'one':disease_one,'two':disease_two,'three':disease_three})

    else:
        return redirect('/account/login')

def LogoutUser(request) :
    if request.method == 'GET':
        logout(request)
        messages.success(request, 'Logout successfully!')
        return redirect('/account/login')


def Profile(request):
    if request.method == 'GET' :
        if request.user.is_authenticated and request.user.is_staff==False:
            profile = CreateUser.objects.get(user=request.user)
            context = {
                'profile' : profile
            }
            return render(request, 'profile.html', context)
        elif request.user.is_authenticated and request.user.is_staff==True:
            profile = CreateUser.objects.get(user=request.user)
            context = {
                'profile' : profile
            }
            return render(request, 'profile.html', context)
        else :
            return redirect('/account/login')
    elif request.method == 'POST' :
        fname = request.POST['first_name']
        lname = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone_number']
        if fname == "":
            messages.error(request, "Please fill out first name!")
            return redirect('/profile')
        elif lname == "":
            messages.error(request, "Please fill out last name!")
            return redirect('/profile')
        elif password == "":
            messages.error(request, "Please fill out password!")
            return redirect('/profile')
        elif len(password) < 8:
            messages.error(request, "Password length will be at least minimum 8 character!")
            return redirect('/profile')
        elif phone == "":
            messages.error(request, "Please fill out phone no!")
            return redirect('/profile')
        elif User.objects.filter(username=email).exists() and request.user.username!=email :
            messages.error(request, "This email already exists.")
            return redirect('/profile')
        else :
            profile = CreateUser.objects.get(user=request.user)
            user = User.objects.get(id=request.user.id)
            user.username = email
            user.set_password(password)
            user.save()
            profile.userfirstname = fname
            profile.userlastname = lname
            profile.userphone = phone
            profile.save()
            login(request, user)
            messages.success(request, "Profile updated successfully.")
            return redirect('/profile')

