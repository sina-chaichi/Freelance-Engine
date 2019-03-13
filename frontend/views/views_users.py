from django.shortcuts import render
from users.forms import UserForm,UserProfileInfoForm
from django.contrib.auth.models import User

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


#home page
def index(request):
    return render(request,'index.html')


# register part

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'related/register.html',
                                          {'user_form':user_form,
                                           'profile_form':profile_form,
                                           'registered':registered})




#login part

def get_user(email):
    try:
        return User.objects.get(email=email.lower())
    except User.DoesNotExist:
        return None

def user_login(request):
    loggedin = False

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = get_user(email)


        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return JsonResponse({
                'status':True,
                'message' : 'Wlcome {}'.format(username)})
                loggedin = True
                print(loggedin)
            else:
                return JsonResponse({
                'status':False,
                'message' : 'You are noy activated'})
        else:
            print('Someone tried to login and failed')
            print('Email: {} and Password: {}'.format(email,password))
            return JsonResponse({
            'status':False,
            'message' : 'Your username and password did not mach. Try again' })
    else:
        return render(request,'related/login.html',{})



#logout part

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
