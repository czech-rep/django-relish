from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm 
        # commented bc we replaced UserCreationForm with ours
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created. You can now log in') 
                        # remember to put in html place for messages to appear
                        # we put it in base above content block
                        # tags of messages in bootstrap match tags in django
                        # so we extract there .tags to get nice formatting
            return redirect('login') # here u enter 'name' attrib from urls
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

    # cool that we can extend template form blog folder, like here:
    # {% extends "blog/base.html" %}

    # next, we add csrf token - some kond of security that django requires
    # message.debug
    # info success warning error = types of messagesk

    # form:form is given to html. next, form is printed as {% form.as_p %}

from django.contrib.auth.decorators import login_required 

@login_required
def profile(request):
    if request.method == 'POST': # showed after POST = given new data
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'account updated')
            return redirect('profile')
            # post get redirect pattern = thats why u want to redirect out from here 
            # same as when refreshing after post request

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile) 
        # instance to populate those forms with current info
        # so, whats request? is it a current dictionary
        # !! do sprawdzenia, co to te pobierane argumenty ? 

    context = {
        'u_form': u_form,
        'p_form': p_form # we put two forms into one html form for user to see them as one
    }
    return render(request, 'users/profile.html', context)
    # remember about special encoding type
    # for forms to load image data properly
    # enctype="multipart/form-data" added to <form > tag 
    