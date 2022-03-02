from django.contrib.sitemaps import Sitemap

from blog.models import Articles

class ArticlesSitemap(Sitemap):
		changefreq = "weekly"
		priority = 0.9
		
		def items(self):
				return Articles.objects.all()
		
		def lastmod(self, obj):
				return obj.update_date