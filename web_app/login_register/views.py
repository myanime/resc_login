from django.shortcuts import render
from forms import LoginForm
from .register_logon import start_login, start_register


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        mysite = form.data['dropdown_list']
        print mysite
        context = {"message":"The Script is logging on...", "form":form}
        start_login(mysite)

        return render(request, "login_register/login.html", context=context)
    else:
        form = LoginForm()
        context = {"form": form}
        return render(request, "login_register/login.html", context=context)

def register(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        mysite = form.data['dropdown_list']
        context = {"message":"The Script is registering...", "form":form}
        start_register(mysite)
        return render(request, "login_register/register.html", context=context)
    else:
        form = LoginForm()
        context = {"form": form}
        return render(request, "login_register/register.html", context=context)
def index(request):
    return render(request, "login_register/index.html")
