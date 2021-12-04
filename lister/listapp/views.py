import re

from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import response
from django.core.exceptions import ValidationError
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .models import Item, Code
from .forms import (AddItemForm, SignUpInitForm, SignUpCheckForm, SignUpForm, 
                ResetPassInitForm, ResetPassCheckForm, ResetPassChangeForm)
from .sort import Sort
from .accproc import AccountProc


types = dict(Item.TYPE)

def index(request):
    if request.user.is_authenticated:
        current_user = request.user
        items = Sort.sort_items_default(current_user)
        return render(request, 'listapp/index.html', 
                        {'items': items, 'types': types})
    else:
        return render(request, 'listapp/index.html')

@login_required()
def index_sort(request, key):
    current_user = request.user
    items = Sort.sort_items_by_param(key, current_user)
    return render(request, 'listapp/index.html', 
                    {'items': items, 'types': types})

@login_required()
def index_search(request):
    current_user = request.user
    key = request.GET.get('query')
    regexp = re.compile('[^0-9a-zA-Z +]+')
    if regexp.search(key):
        items = Sort.sort_items_default(current_user)
    else:
        items = Sort.search_item(key, current_user)
    return render(request, 'listapp/index.html', 
                            {'items': items, 'types': types})

def about(request):
    if request.user.is_authenticated:
        current_user = request.user
        items = Item.objects.filter(item_author = current_user)
        items_today = Sort.sort_items_today(current_user)
        items_statistic = {
            'items_today': items_today,
            'items_today_count': items_today.count(),
            'items_active_count': items.count(),
            'items_executed_count': items.filter(item_isdone = "yes").count(),
            'items_nexecuted_count': items.filter(item_isdone = "no").count(),
            'items_popular_types': Sort.sort_types_popular(current_user),
        }
        return render(request, 'listapp/about.html', 
                        {'items_statistic': items_statistic})
    else:
        return render(request, 'listapp/about.html')

@login_required()
def item_new(request):
    if request.method == "POST":
        form = AddItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.item_author = request.user
            item.item_created = timezone.now()
            item.save()
            return render(request, 'listapp/item_new.html', {'form': form})
    else:
        form = AddItemForm()
    return render(request, 'listapp/item_new.html', {'form': form})

@login_required()
def item_edit(request, pk):
    try:
        item = Item.objects.filter(item_author = request.user).get(pk=pk)
    except:
        return redirect('page_404')
    if request.method == "POST":
        form = AddItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.item_author = request.user
            item.save()
            return render(request, 'listapp/item_edit.html', {'item': item, 'form': form})
    else:
        form = AddItemForm(instance=item)
    return render(request, 'listapp/item_edit.html', {'item': item, 'form': form})

@login_required()
def item_delete(request, pk):
    try:
        item = Item.objects.filter(item_author = request.user).get(pk=pk)
    except:
        return redirect('page_404')
    if request.method == "POST":
        item.delete()
        return redirect('index')
    return render(request, 'listapp/item_delete.html', {'item': item})

def signup_init(request):
    if request.method == 'POST':
        form = SignUpInitForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if AccountProc.ban_email(email):
                return redirect('page_signup_ban')
            else:
                token = AccountProc.initiate_proc(email)
                response = redirect('signup_check')
                response.set_cookie('pass_token', token, max_age=3600)
                return response
    else:
        form = SignUpInitForm()
    return render(request, 'listapp/signup_init.html', {'form': form})

def signup_check(request):
    token = request.COOKIES.get('pass_token')
    if AccountProc.get_step(token) == 0:
        if request.method == 'POST':
            form = SignUpCheckForm(request.POST)
            if form.is_valid():
                user_code = form.cleaned_data['code_value']
                if AccountProc.check_proc(user_code, token):
                    response = redirect('signup')
                    response.set_cookie('pass_token', token, max_age=3600)
                    AccountProc.set_step(token, 1)
                    return response
                else:
                    return redirect('page_error')
            else:
                ban_err = AccountProc.ban_code(token)
                if ban_err == 1:
                    return redirect('page_signup_ban')
                elif ban_err == 2:
                    return redirect('page_error')
        else:
            form = SignUpCheckForm()
        return render(request, 'listapp/signup_check.html', {'form': form})
    else:
        return redirect('page_404')

def signup(request):
    token = request.COOKIES.get('pass_token')
    if AccountProc.get_step(token) == 1:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                if AccountProc.check_token(token):
                    sigform = form.save()
                    email = AccountProc.get_email(token)
                    user = User.objects.get(username=sigform.username)
                    user.email = email
                    user.save()
                    AccountProc.clear_proc(email)
                    response = redirect('signup_success')
                    response.delete_cookie('pass_token')
                    return response
                else:
                    return redirect('page_error')
        else:
            form = SignUpForm()
        return render(request, 'listapp/signup.html', {'form': form})
    else:
        return redirect('page_404')

def signup_success(request):
    return render(request, 'listapp/signup_success.html')

@login_required()
def profile(request):
    username = request.user
    email = request.user.email
    return render(request, 'listapp/profile.html', 
                    {'username': username, 'email': email})

@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('change_password_success')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'listapp/change_password.html', {'form': form})

@login_required()
def change_password_success(request):
    return render(request, 'listapp/change_password_success.html')

def reset_password(request):
    if request.method == 'POST':
        form = ResetPassInitForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if AccountProc.ban_email(email):
                return redirect('page_reset_ban')
            else:
                token = AccountProc.initiate_proc(email)
                response = redirect('reset_password_check')
                response.set_cookie('pass_token', token, max_age=3600)
                return response
    else:
        form = ResetPassInitForm()
    return render(request, 'listapp/reset_password.html', {'form': form})

def reset_password_check(request):
    token = request.COOKIES.get('pass_token')
    if AccountProc.get_step(token) == 0:
        if request.method == 'POST':
            form = ResetPassCheckForm(request.POST)
            if form.is_valid():
                user_code = form.cleaned_data['code_value']
                if AccountProc.check_proc(user_code, token):
                    response = redirect('reset_password_change')
                    response.set_cookie('pass_token', token, max_age=3600)
                    AccountProc.set_step(token, 1)
                    return response
                else:
                    return redirect('page_error')
            else:
                ban_err = AccountProc.ban_code(token)
                if ban_err == 1:
                    return redirect('page_reset_ban')
                elif ban_err == 2:
                    return redirect('page_error')
        else:
            form = ResetPassCheckForm()
        return render(request, 'listapp/reset_password_check.html', 
                        {'form': form})
    else:
        return redirect('page_404')

def reset_password_change(request):
    token = request.COOKIES.get('pass_token')
    if AccountProc.get_step(token) == 1:
        if request.method == 'POST':
            form = ResetPassChangeForm(request.POST)
            if form.is_valid():
                if AccountProc.check_token(token):
                    email = AccountProc.get_email(token)
                    user = User.objects.get(email=email)
                    user.set_password(form.cleaned_data['new_password1'])
                    update_session_auth_hash(request, user)
                    user.save()
                    AccountProc.clear_proc(email)
                    response = redirect('reset_password_success')
                    response.delete_cookie('pass_token')
                    return response
                else:
                    return redirect('page_error')
        else:
            form = ResetPassChangeForm()
        return render(request, 'listapp/reset_password_change.html', 
                        {'form': form})
    else:
        return redirect('page_404')

def reset_password_success(request):
    return render(request, 'listapp/reset_password_success.html')

def page_404(request, exception):
    data = {}
    return render(request, 'listapp/404.html', data)

def page_500(request):
    return render(request, 'listapp/404.html')

def page_error(request):
    return render(request, 'listapp/error.html')

def page_signup_ban(request):
    return render(request, 'listapp/ban_signup.html')

def page_reset_ban(request):
    return render(request, 'listapp/ban_reset.html')

def page_login_ban(request):
    return render(request, 'listapp/ban_login.html')
