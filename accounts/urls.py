from django.urls import path
from . import views

from django.contrib.auth.decorators import login_required

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('<str:username>/', views.profile, name='profile'),
    path('<str:username>/follow/', views.follow, name='follow'),
    path('<str:username>/profile_update/', login_required(views.ProfileUpdateView.as_view()), name='profile_update'),
    path('<str:username>/followerswings/', views.followerswings, name='followerswings'),
    path('<str:username>/account_update/', login_required(views.AccountUpdateView.as_view()), name='account_update'),
]