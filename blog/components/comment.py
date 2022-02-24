from unicodedata import name
from django_unicorn.components import UnicornView
from ..models import Comments , Articles

class CommentView(UnicornView):
    email : str = ''
    name : str = ''
    body : str = ''
    article: Articles = None
    comments : Comments = None


    def mount(self):
        id = self.request.path.split('/')[-1]
        self.article = Articles.objects.get(id = id)
        print('votre request')
        print(id)
        print(self.article.title)
        return super().mount()
