from django.contrib import admin
from portfolio.models import*


class FormationAdmin(admin.ModelAdmin):
     list_display = ['name', 'description', 'start_at', 'end_at']
admin.site.register(Formation , FormationAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'publish_at',]
admin.site.register(Project , ProjectAdmin)

class TechnoAdmin(admin.ModelAdmin):
    list_display = ['name', 'level',]
admin.site.register(Techno , TechnoAdmin)

class LangueAdmin(admin.ModelAdmin):
    list_display = ['name', 'level',]
admin.site.register(Langue , LangueAdmin)

class InteretAdmin(admin.ModelAdmin):
    list_display = ['name',]
admin.site.register(Interet , InteretAdmin)

class QualityAdmin(admin.ModelAdmin):
    list_display = ["name",]
admin.site.register(Quality, QualityAdmin)

class ExprienceProfAdmin(admin.ModelAdmin):
    list_display = ['type','description', 'start_at', 'end_at', 'etablisement',]
admin.site.register(ExperienceProf , ExprienceProfAdmin)

class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['email', 'date',]
admin.site.register(Newsletter , NewsletterAdmin)