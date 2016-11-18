import os

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .form import LoginForm, SignUpForm, VideoResponseForm
from .models import User,ResponseFile

from .s3.s3 import upload_original_to_s3
from .sqs.add_to_sqs import add_video_file_for_encoding
from .transcoder.create_job import set_transcoder_job

@login_required
def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = VideoResponseForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = ResponseFile(docfile = request.FILES['docfile'],
                                  user_id=request.user.id)

            newdoc.save()

            # renames user_timestamp.ext and uploads to S3
            bucket_name, filename = upload_original_to_s3(newdoc.docfile, request.user)
            # sqs, dont do much yet
            add_video_file_for_encoding(bucket_name, filename, request.user.username)
            # instead, we create transcoder job here
            set_transcoder_job(filename)
            return HttpResponseRedirect(reverse('index'))
    else:
        form = VideoResponseForm() # A empty, unbound form

    # Load documents for the list page
    documents = ResponseFile.objects.all()
    users = User.objects.all()
    # Render list page with the documents and the form
    return render(request, "ninja/upload.html", {'documents': documents,
                                                 'users':users,
                                                 'form': form} )





def user_login(request):
    # if successful redirects to index
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])

            if user is not None:

                if user.is_active:
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, 'Authorization successful.')
                    return redirect('index')

                else:
                    messages.add_message(request, messages.INFO, 'This user is suspended')
                    return render(request, 'ninja/login.html', {'form': form})
            else:
                messages.add_message(request, messages.WARNING, 'Authorization FAILED.')
                return render(request, 'ninja/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'ninja/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


def user_sign_up(request):

    def user_exists(username):
        return User.objects.filter(username=username).exists()

    # Reinventing the bicycle for educational purposes
    #   in production should use django validation.
    #   Creates the most basic user, without any confirmations
    #   and with very limited validation
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            if user_exists(cd['username']):
                messages.add_message(request, messages.WARNING, 'User exists. Please chose different username')
                return render(request, 'ninja/signup.html', {'form': form})

            if cd['password'] != cd['password_repeat']:
                messages.add_message(request, messages.WARNING, 'Passwords do NOT match')
                return render(request, 'ninja/signup.html', {'form': form})

            u = User(username=cd['username'], email=cd['password'])
            u.set_password(cd['password'])
            u.save()

            messages.add_message(request, messages.SUCCESS, 'SignUp successful! Please login')
            return redirect('login')


        # if form is not valid, whatever that means
        else:
            messages.add_message(request, messages.WARNING, 'Form validation failed << DEBUG purposes')
            return render(request, 'ninja/signup.html', {'form': form})
    # if method == 'GET' just display the form
    else:
        form = SignUpForm()
        return render(request, 'ninja/signup.html', {'form': form})