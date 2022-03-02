from django.http import BadHeaderError
from portfolio.models import Newsletter
from portfolio.forms import NewsletterForm
from django.contrib import messages
from django.core.mail import send_mail

def newsletter_form(request):

    newsform = NewsletterForm()

    if request.method == "POST":
        if 'news_letter' in request.POST:
            newsform = NewsletterForm(request.POST)
            if newsform.is_valid():
                try:
                    send_mail(
                    subject="02xcode Newsletter",
                    message="Merci pour votre inscription",
                    from_email= "contact@02xcode.com",
                    recipient_list=[newsform.cleaned_data['email']]
                    )
                    newsform.save()
                    newsform = NewsletterForm()
                    messages.success(request, 'vous avez bien été inscris !')
                except BadHeaderError:
                    messages.error(request, 'Votre inscription a échoué')
    return newsform
