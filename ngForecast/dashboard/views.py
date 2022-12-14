from django.shortcuts import render, redirect, reverse

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

import pandas as pd
from .utils import fetch_news, encode_plot, plot_graphs, predict_close, key_data, df, nas


news24 = fetch_news()
line_plot, dist_plot, sm_plot = plot_graphs()
trend, error = predict_close()


def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard:home'))
    else:
        registration_form = UserCreationForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                messages.success(request, f"Account created for {user} :)")
                return redirect(reverse('dashboard:login'))
            messages.error(request, "Registration was unsuccessful:(")

        return render(request, "dashboard/register.html", {
            "form": registration_form
        })


def signin(request):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard:home'))
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            passwd = request.POST.get('password')
            user = authenticate(request, username=username, password=passwd)
            if user is not None:
                login(request, user)
                return redirect(reverse('dashboard:home'))
            else:
                messages.error(request, f"Account does not exist..\nPlease do register")
                return redirect(reverse('dashboard:register'))
        return render(request, "dashboard/login.html", {
        })


@login_required(login_url="dashboard:login")
def signout(request):
    logout(request)
    return redirect(reverse('dashboard:login'))



@login_required(login_url="dashboard:login")
def urlredirect(request):
    return redirect(reverse('dashboard:dashboard'))


@login_required(login_url="dashboard:login")
def dashboard(request):
    global trend
    global error

    keys = key_data()
    
    accuracy =  100 - error*100
    return render(request, "dashboard/dashboard.html", {
        "trend": encode_plot(trend),
        "accuracy": round(accuracy, 3),
        "keys": keys,
        })  




prev_no = 1
page_no = 1
@login_required(login_url="dashboard:login")
def history(request, page="1"):
    global prev_no
    global page_no

    prev_no = page_no
    print(page_no)
    
    file_path1 = "C:/Users/devas/Documents/projects/natural-gas-forecasting/ngForecast/dashboard/static/dashboard/processed_nasdaq.csv"
    nas = pd.read_csv(file_path1, parse_dates=True)
    nas = nas.drop(["vol"], axis=1)

    columns = [col for col in nas.columns]
    rows = [row for row in (nas.values[::-1])] 

    pages = [rows[i:i+30] for i in range(0, len(rows), 30)]
    print("No of pages will be: ", len(pages))

    if page == 'n':
        page_no = (page_no + 1)% len(pages)
    elif page == 'p':
        if page_no == 0:
            page_no =len(pages)-1
        else:
            page_no = (page_no-1)%len(pages)
    else:
        page_no = int(page)

    keys = key_data()

    return render(request, 'dashboard/history.html', {
        'cols': columns,
        'rows': pages[page_no],
        'prev_page': prev_no,
        "keys": keys,
    })





@login_required(login_url="dashboard:login")
def daily_news(request):
    return render(request, "dashboard/news.html", {
        "news24": news24,
    })



@login_required(login_url="dashboard:login")
def trends(request):
    global line_plot
    global news24

    return render(request, "dashboard/trends.html", {
        "lp": encode_plot(line_plot),
        "news24": news24[:5],
    })



@login_required(login_url="dashboard:login")
def concrete(request):
    global df
    global dist_plot
    global sm_plot

    return render(request, "dashboard/concrete.html", {
        "dp": encode_plot(dist_plot),
        "sp": encode_plot(sm_plot),
    })

