from . import views
from django.urls import path

app_name = "dashboard"

urlpatterns = [
    path("", views.urlredirect, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.signin, name="login"),
    path("logout/", views.signout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("history/", views.history, name="history"),
    path("history/<str:page>/", views.history, name="history_pages"),
    path("trends/", views.trends, name="trends"),
    path("concrete/", views.concrete, name="concrete"),
    path("daily_news/", views.daily_news, name="news"),
]
