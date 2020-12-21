from django.views import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import SignInUserForm, RegisterUsername
from .models import NMUser



class Home(View):
    def get(self, request):
        request.session.set_expiry(300)
        user = request.session.get('user')
        name = request.session.get('name')
        loginForm = SignInUserForm()
        return render(request, 'NuMe/index.html', {
            "loginForm": loginForm,
            "user": user,
            "name": name
        })

    def post(self, request):
        request.session.set_expiry(300)
        loggedInFlag = 1
        loginForm = SignInUserForm()
        f = SignInUserForm(request.POST)
        if f.is_valid():
            username = f.cleaned_data['username']
            password = f.cleaned_data['password']
            try:
                request.session.set_expiry(300)
                validUser = NMUser.objects.get(
                    username=username, password=password)
                request.session['user'] = validUser.username
                request.session[
                    'name'] = validUser.firstName + ' ' + validUser.lastName
                user = request.session.get("user")
                name = request.session.get('name')
                print(name)
                print(user)
                print(loggedInFlag)
                return render(request, "NuMe/index.html", {
                    "user": user,
                    "name": name,
                    "loggedInFlag": loggedInFlag
                })
            except NMUser.DoesNotExist:
                loggedInFlag = 0
                msg = 'Username and password combination does not exist.'
                return render(request, 'NuMe/index.html', {
                    "loginForm": loginForm,
                    'msg': msg
                })
        else:
            loggedInFlag = 0
            loginForm = SignInUserForm()
            return render(request, "NuMe/index.html", {
                "loginForm": loginForm,
                "loggedInFlag": loggedInFlag
            })


class Register(View):
    def get(self, request):
        request.session.set_expiry(300)
        f = RegisterUsername()
        return render(request, 'NuMe/registration/register.html', {"f": f})

    def post(self, request):
        request.session.set_expiry(300)
        f = RegisterUsername(request.POST)
        if f.is_valid():
            new_user = f.save()
            new_user = authenticate(
                username = f.cleaned_data['username'],
                password = f.cleaned_data['password']
            )
            login(request, new_user)
            successMsg = 'Account successfully created.'
            return render(request, "NuMe/registration/register.html", {"successMsg": successMsg})
        else:
            errorMessage = 'Username Taken'
            return render(request, 'NuMe/registration/register.html', {
                "f": f,
                "errorMessage": errorMessage
            })


class User(View):
    def get(self, request):
        request.session.set_expiry(300)
        user = request.session.get("user")
        print(user)
        loginMessage = 'Please sign in to use this feature.'
        print(loginMessage)
        return render(request, "NuMe/user.html", {
            "user": user,
            "loginMessage": loginMessage
        })
