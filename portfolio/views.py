from email import message
from django.contrib import messages
from django.shortcuts import get_object_or_404, render
from blog.models import Articles
from blog.views import articles
from portfolio.forms import ContactForm, NewsletterForm
from portfolio.models import*
from django.core.mail import send_mail
from classes.methods import newsletter_form

# Create your views here.

def portfolio(request):
    newsform = newsletter_form(request)
    return render(request, 'home.html', context={"newsform":newsform})

def cv(request):
    newsform = newsletter_form(request)
    formation = Formation.objects.all()
    techno = Techno.objects.all()
    langue = Langue.objects.all()
    interet = Interet.objects.all()
    experience = ExperienceProf.objects.all()
    quality = Quality.objects.all()
    context={
        'formations':formation, 
        'technos':techno , 
        'langues':langue,
        "interets":interet,
        "experience":experience,
        "qualitys":quality,
        "newsform":newsform
         }
    return render(request, 'cv.html', context)

def projects(request):
    newsform = newsletter_form(request)
    projects = Project.objects.all()
    return render (request, 'projects.html', context = {'projects':projects, "newsform":newsform})

def contact(request):

    newsform = newsletter_form(request)
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            send_mail(subject=f'Envoyer par {form.cleaned_data["full_name"] or "anonyme"}',
            message = form.cleaned_data["message"],
            from_email = form.cleaned_data["email"],
            recipient_list=['cs.ttrx@gmail.com']
            )
            messages.success(request, 'Votre message a bien été envoyé ! merci allons vous repondre bientot')
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, 'contact.html', context={"form":form, "newsform":newsform})

def newsletter(request):
    form = newsletter_form(request)

    return render(request, 'newsform.html', context= {"news_form": form})
