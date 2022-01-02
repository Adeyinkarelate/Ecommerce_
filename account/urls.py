from django.urls import path
from . import views 

urlpatterns =[
    path('register/', views.register , name="register"),
    path('login/', views.login , name="login"),
    path('logout/', views.logout , name="logout"),
]

# ading the account to the main urls 
# path('account/' , include('account.urls')),