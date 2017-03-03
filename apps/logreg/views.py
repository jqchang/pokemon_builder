from django.shortcuts import render, redirect
from .models import User, Pokemon
from django.contrib import messages
# Create your views here.
def start(request):
    return render(request, 'logreg/start.html')

def prof(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = -1
    return render(request, 'logreg/login.html')

def login(request):
    print "**LOGIN**"
    if request.method == 'GET':
        print "** Login is POST-only **"
        return redirect('/')
    print "** Log in requested **"
    login_info = User.objects.login(**request.POST)
    if login_info['valid']:
        print "** Login info is valid **"
        request.session['user_id'] = login_info['user_id']
        return redirect('/roster')
    else:
        print "** Something went wrong **"
        for msg in login_info['messages']:
            messages.warning(request, msg)
        return redirect('/prof')

def register(request):
    if request.method == 'GET':
        print "** Registration is POST-only **"
        return redirect('/')
    print "** Registration requested **"
    status_info = User.objects.register(**request.POST)
    if status_info['valid']:
        print "** Registration information is valid **"
        for msg in status_info['messages']:
            messages.success(request, msg)
    else:
        print "** Something went wrong **"
        for msg in status_info['messages']:
            messages.error(request, msg)
    return redirect('/prof')

def success(request):
    if 'user_id' not in request.session or request.session['user_id'] == -1:
        print "Nuh-uh. You can't see this page yet."
        request.session['user_id'] = -1
        messages.warning(request, 'Please sign-in or register.')
        return redirect('/prof')
    else:
        print "**WELCOME TO THE JUNGLE**"
        return redirect('/teambuilder')

def logout(request):
    if request.method == "GET":
        print "Logging out should be a POST request"
        return redirect('/')
    print "** Logging out **"
    request.session.pop('user_id')
    return redirect('/')
