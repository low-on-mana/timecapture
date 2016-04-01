from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login,logout,authenticate
from .models import TimeUserForm,TimeUser
from django.contrib.auth.decorators import login_required

def index(request):
    if request.user.is_authenticated():
        return redirect('timesheet:index')
    return render(request,'timecapture/login.html')

def auth_login(request):
    if request.user.is_authenticated():
        return redirect('timesheet:index')
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email,password=password)
        if user is not None:
            if user.is_active:
                user_last_login = user.last_login
                login(request,user)
                if user_last_login is None:
                    request.session['firsttime'] = 'yes'
                    return redirect(reverse_lazy('auth_info'))
                return redirect('timesheet:index')
            else:
                error = "Your account has been disabled by the administrator"
        else:
            error = "Incorrect username/password"
    else:
        return render(request,'timecapture/login.html')
    return render(request,'timecapture/login.html',{'error':error})


def auth_logout(request):
    logout(request)
    return render(request,'timecapture/login.html')

@login_required
def auth_info(request):
    timeuser = TimeUser.objects.get(pk=request.user.id)
    firsttime  = False
    if 'firsttime' in request.session:
        firsttime = True
        del request.session['firsttime']

    form = TimeUserForm(request.POST or None,instance=timeuser)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('timesheet:index')

    return render(request,'timecapture/info.html',{'firsttime':firsttime,'form':form})
