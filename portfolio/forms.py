import email
from django import forms
from portfolio.models import Newsletter

class ContactForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={"class":'form_input', "placeholder":"Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form_input', "placeholder":"Your Email"}))
    message = forms.CharField(widget= (forms.Textarea(attrs = {'class':'form_textarea', "placeholder":"Enter your message here"})))

class NewsletterForm(forms.ModelForm):
    news_letter = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'news-input',
        "placeholder":"Adress mail",
    }))
    class Meta:
        model = Newsletter
        fields = ["email",'news_letter',]