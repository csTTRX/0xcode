from dataclasses import fields
import email
from logging import PlaceHolder
from multiprocessing.sharedctypes import Value
from unicodedata import category
from django import forms
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from blog.models import Articles, Comments
class SearchForm(forms.Form):
    Value = forms.CharField(widget=forms.TextInput(attrs={'class' : "search_value" ,'name':'value', 'placeholder':'Recherher'}))

class ArticleForm(forms.ModelForm):
    title =forms.CharField(widget=forms.TextInput(attrs={'class' : "art-input" ,'placeholder':'Le titre'}))
    title_tags =forms.CharField(widget=forms.TextInput(attrs={'class' : "art-input" ,'placeholder':'Les tags'}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class" : "form_textarea", "placeholder":"Description"}))
    #publish = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class" : "art-input", "label":"Publier maintenant"}))
    class Meta:
        model = Articles
        fields = ['title', 'title_tags', 'body','categories', 'description','publish',]
    
    def __init__(self, *args, **kwargs):
        super(ArticleForm,self ).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs={"class":'art-body', 'placeholder':'Le contenu de votre article'}
        self.fields['categories'].widget.attrs={"class":'art-cat', 'placeholder':'choisisez une categorie'}
        #self.fields['publish'].widget.attrs={"class":'art-input', 'label':'Publier maintenant'}


class CommentForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class" : "cmt-input", "placeholder":"Email"}))
    name = forms.CharField(widget=forms.TextInput(attrs={"class" : "cmt-input", "placeholder":"Nom"}))
    body = forms.CharField(widget=forms.Textarea(attrs={"class" : "form_textarea", "placeholder":"votre commentaire"}))
    class Meta:
        model = Comments
        fields = ('name', 'email', 'body')