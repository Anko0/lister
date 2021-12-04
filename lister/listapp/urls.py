from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('sort/<str:key>/', views.index_sort, name='index_sort'),
    path('search/', views.index_search, name='index_search'),
    path('about/', views.about, name='about'),
    path('item/new/', views.item_new, name='item_new'),
    path('item/edit/<int:pk>/', views.item_edit, name='item_edit'),
    path('item/delete/<int:pk>/', views.item_delete, name='item_delete'),
    path('profile/', views.profile, name='profile'),
    path('signup_init/', views.signup_init, name='signup_init'),
    path('signup_check/', views.signup_check, name='signup_check'),
    path('signup/', views.signup, name='signup'),
    path('signup_success/', views.signup_success, name='signup_success'),
    path('change_password/', views.change_password, name='change_password'),
    path('change_password_success/', views.change_password_success, 
                                    name='change_password_success'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('reset_password_check/', views.reset_password_check, 
                                    name='reset_password_check'),
    path('reset_password_change/', views.reset_password_change, 
                                    name='reset_password_change'),
    path('reset_password_success/', views.reset_password_success, 
                                    name='reset_password_success'),
    path('404/', views.page_404, name='page_404'),
    path('error/', views.page_error, name='page_error'),
    path('signup_ban/', views.page_signup_ban, name='page_signup_ban'),
    path('reset_ban/', views.page_reset_ban, name='page_reset_ban'),
    path('login_ban/', views.page_login_ban, name='page_login_ban'),
]
