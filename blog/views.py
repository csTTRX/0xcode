import datetime
import profile
from sqlite3 import connect
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from blog.models import Articles, SiteInfo
from classes.methods import newsletter_form
from blog.forms import ArticleForm ,CommentForm
from portfolio.forms import ContactForm
from django.shortcuts import render, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site 
from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.db.models import Q


def blog(request):
    newsform = newsletter_form(request)
    news_articles = Articles.objects.order_by("-update_date")[:6]
    return render(request, 'blog_home.html', context= {'newsform':newsform, 'news_articles':news_articles})

    
def articles(request):
    newsform = newsletter_form(request)
    article = Articles.objects.all()
    paginator = Paginator(article, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
            
    return render(request, 'blog.html', context={'newsform':newsform, 'page_obj':page_obj})


def show_article(request , id):
    tags = []
    comment_form = CommentForm()
    newsform = newsletter_form(request)
    article = Articles.objects.get(id = id)
    comments = article.comments.filter(publish = True)
    new_comment = None
    facebook_url = article.author.profile.facebook_url
    twitter_url = article.author.profile.twitter_url
    instagram_url = article.author.profile.instagram_url 
    linkedin_url = article.author.profile.linkedin_url
    github_url = article.author.profile.github_url
    photo = article.author.profile.photo
    bio = article.author.profile.biograph
    author_name = article.author.username
    tags = article.title_tags.split(',')

    if request.method == 'POST':

        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article_id = article.pk
            new_comment.articles = article
            new_comment.save()
            comment_form = CommentForm()
    context={
        'newsform':newsform,
        'article':article,
        'facebook_url':facebook_url,
        'twitter_url':twitter_url,
        'instagram_url':instagram_url,
        "linkedin_url":linkedin_url,
        "github_url":github_url,
        "photo":photo,
        "bio":bio,
        "author_name":author_name,
        "tags":tags,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    }

    return render(request, 'show_article.html', context)

@login_required()
@permission_required('blog.add_articles', raise_exception=True)
def add_article(request):
    newsform = newsletter_form(request)
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.post_date = datetime.datetime.now()
            article.save()
            messages.success(request, "Votre Article a bien été ajouté ! continuez d'ajouter")
            form = ArticleForm()
    return render(request, 'add_article.html', context ={'newsform':newsform,'article_form':form})

def blog_search(request):
    newsform = newsletter_form(request)
    if request.method == "POST":
        find = False
        searched = request.POST['searched']
        result = Articles.objects.filter(title__contains = searched)
        if len(result) > 0:
            find = True
            """paginator = Paginator(result, 100)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)"""
            
        return render(request, 'blog_search.html', context={'newsform':newsform, "results":result, "searched":searched, "find":find})
    else:

         return render(request, 'blog_search.html', context={'newsform':newsform, "results":result})


def blog_contact(request):

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
    return render(request, 'blog_contact.html', context={"form":form, "newsform":newsform})

def about(request):
    newsform = newsletter_form(request)
    about = get_object_or_404(SiteInfo, title_tags = "about" )

    return render(request, 'about.html', context={"about":about, "newsform":newsform})

def politique(request):
    newsform = newsletter_form(request)
    politique = get_object_or_404(SiteInfo, title_tags = "politique")
    return render(request, 'politique.html', context={"politique":politique, "newsform":newsform})

def dashbord(request):
    author_articles = Articles.objects.filter(Q(author = request.user)).order_by('id')
    print(request.user.profile.pk)
    return render(request, 'dashbord2.html', context={'author_articles':author_articles})

def delete(request, id):
    article = get_object_or_404(Articles, id = id)
    del_form = ArticleForm(instance = article)
    if request.method == "POST":
        del_form = ArticleForm(request.POST, instance = article)
        article.delete()
        messages.error(request, "Votre Article a bien été supprimé")
        return redirect('dashbord')
    return render(request, 'delete.html', context={'del_form': del_form})

def edit(request, id):
    article = get_object_or_404(Articles, id = id)
    edit_form = ArticleForm(instance = article)
    if request.method == "POST":
        edit_form = ArticleForm(request.POST, instance = article)
        edit_form.save()
        messages.success(request, 'Votre Article a bien été modifié')
        #return redirect('dashbord')
    return render(request, 'edit.html', context={'article_form': edit_form})