from django.contrib import admin

from blog.models import Articles, Categories, Outils, Comments, SiteInfo

class ArticleAdmin(admin.ModelAdmin):

    list_display = ["title", "title_tags", "post_date", 'categories','description', ]
admin.site.register(Articles, ArticleAdmin)
class OutilsAdmin(admin.ModelAdmin):

    list_display = ["name",]

admin.site.register(Outils , OutilsAdmin)

class CategriesAdmin(admin.ModelAdmin):

    list_display = ["name",]

admin.site.register(Categories , CategriesAdmin)

class SiteInfoAdmin(admin.ModelAdmin):

    list_display = ["title", 'title_tags',]

admin.site.register(SiteInfo , SiteInfoAdmin)
# Register your models here.

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'article', 'created_date', 'publish')
    list_filter = ('publish', 'created_date')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(publish=True)