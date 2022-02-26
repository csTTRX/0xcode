from ftplib import error_perm
from gettext import install
from multiprocessing import context
from django.contrib import messages
from django.contrib.auth import login, logout , authenticate
from authentication.authenticate import EmailOrUsernameModelBackend
from django.shortcuts import render, redirect, get_object_or_404
from classes.methods import newsletter_form
from authentication.forms import *
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str as force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from classes.classes import account_activation_token  
from django.contrib.auth.models import User
from authentication.forms import ProfileForm
from django.core.mail import EmailMessage  
from django.http import HttpResponse  

def register(request):

    newsform = newsletter_form(request)
    form = RegisterForm()
    message = ""
    if request.method=='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)  
            to_email = form.cleaned_data.get('email') 
            print(current_site)
            mail_subject = "02xcode.com lien d'activation"
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })   
            email = EmailMessage(  
                        mail_subject, message, to=[to_email]  
            )  
            email.send()  
            return HttpResponse("Veuillez confirmer le lien d'activation envoyé à l'addresse " + to_email)  
    return render(request, 'register.html', context={"form":form,'newsform':newsform})



def login_view(request):

    newsform = newsletter_form(request)
    form = LoginForm()
    if request.method =="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user_authenticated = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password']
            )

            if user_authenticated  is not None:
                login(request, user_authenticated )
                print(request.session)
                return redirect('blog')
    return render(request, 'login.html' , context={'form':form, 'newsform':newsform})


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_text(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        login(request, user)
        return HttpResponse('')  
    else:  
        return HttpResponse('Activation link is invalid!')  


def update_frofile(request, user_id):
    user_id = request.user.profile.user_id
    profile = get_object_or_404(Profile, user_id=user_id)
    profile_form = ProfileForm(instance=profile)
    print(request.user.profile.linkedin_url)
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES , instance = profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'La mise à jour de votre profile a réussi')
    return render(request, 'update_profile.html', context = {'profile_form':profile_form})