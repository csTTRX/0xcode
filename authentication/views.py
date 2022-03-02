from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from classes.methods import newsletter_form
from authentication.forms import *
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str as force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from classes.classes import account_activation_token  
from authentication.forms import ProfileForm
from django.core.mail import EmailMessage  
from django.http import HttpResponse  

from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from authentication.models import User
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator



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
            mail_subject = "02xcode.com lien d'activation"
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })   
            email = EmailMessage(  
                        mail_subject, message, 'contact@02xcode.com', to=[to_email]  
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

            if user_authenticated  is not None and user_authenticated.is_active == True:
                login(request, user_authenticated )
                return redirect('blog')
            else:
                HttpResponse("Votre compte n'est pas encore été activé, Veuillez confirmer votre adresse mail")
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
        messages.success(request, 'Votre compte a bien été activé')
    else:
        return HttpResponse('Votre lien est invalide')


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

def password_reset_request(request):
    newsform = newsletter_form(request)
    current_site = get_current_site(request)

    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':current_site,
                    'site_name': '02xcode',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'contact@02xcode.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalide, veuillez réessayer')
                    return redirect ("password_reset__done")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="password_reset.html", context={"password_reset_form":password_reset_form, "newsform":newsform})