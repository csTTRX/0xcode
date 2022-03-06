"""scPortfolio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from authentication.views import *
from blog.views import *
from portfolio.views import*
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth import views as auth_views
from classes.sitemaps import ArticlesSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
		"articles": ArticlesSitemap,
}

urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('ircsttrx/', admin.site.urls),
    path('', blog, name='blog'),
    path('dashbord/', dashbord, name='dashbord'),
    path('delete/<str:slug>', delete, name='delete'),
    path('edit/<str:slug>', edit, name='edit'),
    path('portfolio/', portfolio, name='portfolio'),
    path('mycv/', cv, name= 'cv'),
    path('projects/', projects, name ='projects'),
    path('projects/<int:id>', projects, name ='projects'),
    path('contact', contact, name = 'contact'),
    path('newletter/', newsletter, name='newsletter'),
    path('articles/', articles, name='articles'),
    path('articles/<str:slug>', show_article, name='show_article'),
    path('search/', blog_search, name='blog_search'),
    path('add_art/', add_article, name='add_article'),
    path('register/', register, name='register'),
    path('contact/', blog_contact, name='blog_contact'),
    path('politique/', politique, name='politique'),
    path('about/', about, name='about'),
    path('login/', login_view, name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('update_profile/<int:user_id>', update_frofile , name="update_frofile"),
    #path('pass_change/', auth_views.PasswordChangeView.as_view(template_name = "password_change.html"), name = "password_change"),
    #path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name = "pass_change_done.html") , name = 'password_change_done'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset__done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'), 
    path("password_reset/", password_reset_request, name="password_reset"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',  activate, name='activate'),  
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("unicorn/", include("django_unicorn.urls")),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root':settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root':settings.MEDIA_ROOT}),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps},
						name='django.contrib.sitemaps.views.sitemap')
]
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
