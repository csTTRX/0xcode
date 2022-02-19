from django_unicorn.components import UnicornView

from blog.views import articles
from ..models import Comments , Articles

class CommentsView(UnicornView):
    article: Articles = None
    comments : Comments = None
    email : str = ''
    name : str = ''
    body : str = ''
    def mount(self):
        id = self.request.path.split('/')[-1]
        self.article = Articles.objects.get(id = id)
        self.comments = Comments.objects.filter(article = self.article)
        return super().mount()
    
    def submit(self):

        Comments.objects.create(
            article_id = self.article.pk,
            email = self.email,
            name = self.name,
            body = self.body,
        )
        self.comments = Comments.objects.filter(article = self.article)
        self.body = ""
        for c in self.comments:
            print(c.created_date)