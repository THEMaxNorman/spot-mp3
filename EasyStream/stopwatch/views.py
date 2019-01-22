from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import subprocess
from models import Profile
import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from stopwatch.forms import SignUpForm
import datetime
import pytz
import time
from background_task import background
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from collections import OrderedDict
import random


from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def home(request):
    if request.method == 'POST':
        url = request.POST.get("url_name")
        com = "spotdl --playlist "
        com += url
        proc = subprocess.Popen(com , stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell = True)
        tmp = proc.stdout.read()

        end = tmp

        o = False
        c = 0
        for x in end:
            c += 1
            if x == 'o':
                break

        word = end[c+1:-1]
        other_com = "spotdl --list "
        other_com += word
        other_com += ' -f ~/Development/EasyStream/media/'
        other_com += word[:-4]
        print other_com

        subprocess.call(other_com, shell = True)
        return redirect('/playlist/'+word[:-4])

    else:






        return render(request, 'home.html',)

def playlist(request, string):
    zip_com = "cd media; zip -vr " + string + ".zip " + string + " -x *.DS_Store"
    print zip_com
    subprocess.call(zip_com, shell=True)
    return render(request, 'playlist.html', {'string' : string})
def signup(request):
    #checks to see if its post or not.
    # if post it validates and the creates new user
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal

            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form , })


def scoreBoardMain(request):
    if request.method == 'POST':
        print "I am doing something"
        #Do something maybe

    else:
        list_of_boards = ["Max", "Max", "Max"]
        #Do Something

    return render(request, 'scoreBoardMain.html', {'end' : list_of_boards})

def scoreBoardSpecific(request, string):
    string = str(string)
    if string == 'football':
        return render(request, "footballScoreboard.html")
    else:
        return render(request, 'home.html', {'string',string} )