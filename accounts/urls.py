from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('', views.index, name="index"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('update/', views.update, name='update'),
    path('password/', views.password_change, name='password_change'),
    path('<int:user_pk>/', views.detail, name='detail'),    # 프로필
    path('<int:user_pk>/delete/', views.delete, name='delete'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('<int:user_pk>/following/', views.following, name='following'),
]