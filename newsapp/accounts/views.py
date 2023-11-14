from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout,update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from .forms import UserRegistrationForm, UserLoginForm, EditProfileForm, InterestsForm
from accounts.models import User, Interest




def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['email'], data['username'], data['password']
            )
            return redirect('accounts:user_login')
    else:
        form = UserRegistrationForm()
    context = {'title':'Signup', 'form':form}
    return render(request, 'register.html', context)


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, email=data['email'], password=data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('Home')
            else:
                messages.error(
                    request, 'email or password is wrong', 'danger'
                )
                return redirect('accounts:user_login')
    else:
        form = UserLoginForm()
    context = {'title':'Login', 'form': form , 'interests': Interest.objects.all()}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('accounts:user_login')


def user_profile(request,userid):
    user = get_object_or_404(User, id=userid)
    context = {'title':'Profile', 'user':user}
    return render(request, 'user_profile.html', context)

@login_required
def edit_profile(request, userid):
    existing_interests = request.user.interests.all()
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            current_password = form.cleaned_data['current_password']
            new_password = form.cleaned_data['new_password']

            if request.user.check_password(current_password):
                if new_password:
                    request.user.set_password(new_password)
                    request.user.save()

                form.save()
                
                updated_interests = request.user.interests.all()
                if existing_interests != updated_interests:
                    user  = request.user
                    cache_key = f'user_home_{user.id}'
                    cache.delete(cache_key)
                update_session_auth_hash(request, request.user)
                
                return render(request, 'user_profile.html', {'user': request.user})
            else:
                form.add_error('current_password', 'Invalid current password')
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})



@login_required
def save_interests(request):
    if request.method == 'POST':
        selected_interests = request.POST.getlist('interests')
        request.user.interests.set(Interest.objects.filter(name__in=selected_interests))
        return redirect('home')
    return redirect('home')
