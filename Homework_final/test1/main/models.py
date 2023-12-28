from django.db import models
#from datetime import datetime
#from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.core.validators import MinLengthValidator, MaxLengthValidator


# Create your models here.

class Product:
    counter = 0

    def __init__(self, title, price, quantiti):
        self.title = title
        self.price = price
        self.quantiti = quantiti
        Product.counter += 1

    def amound(self):
        return self.price * self.quantiti

    def __str__(self):
        return (f" Title->> {self.title}  Price->> {self.price}")

#############################################################################################################

class Account(models.Model):
    gender_choices = (('M', 'Male'),
                      ('F', 'Female'),
                      ('N/A', 'Not answered'))
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                primary_key=True)
    nickname = models.CharField(max_length=100, verbose_name='Ник пользователя')
    birthdate = models.DateField(null=True,  blank=True, verbose_name='День рождения пользователя')
    gender = models.CharField(choices=gender_choices, max_length=20, default='N/A', verbose_name='Пол пользователя')
    account_image = models.ImageField(default='default.jpg',
                                      upload_to='account_images/', verbose_name='Аватар пользователя')


    def __str__(self):
        return f"{self.user.username}'s account"

# удалить потом
    def get_absolute_url(self):
        # return f'/newsall/{self.id}'
        return f'/news_all/'

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class Tag(models.Model):
    title = models.CharField(max_length=80)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def tag_count(self):
        count = self.article_set.count()
        # комментарий: когда мы работаем со связанными объектами (foreign_key, m2m, один к одному),
        # мы можем обращаться к связанным таблицам при помощи синтаксиса:
        # связаннаяМодель_set и что-то делать с результатами. В этом примере - мы используем связанные article
        # и вызываем метод count
        return count

    class Meta:
        ordering = ['title', 'status']
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Article(models.Model):
    categories = (('E', 'Экономика'),
                  ('S', 'Наука'),
                  ('IT', 'Ай-Ти'),
                  ('N', 'Природа'),
                  ('H', 'Хобби'),
                  ('Plk', 'Политика'),
                  ('Rus', 'В России'),
                  ('Pc', 'В мире'),
                  ('Hm', 'Наш край'),
                  ('Km', 'Криминал'),
                  ('Ans', 'Животные'),
                  )
# validators=[validators.EmailValidator(message="Invalid Email")]
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='Автор')
    title = models.CharField(max_length=100, default='', verbose_name='Название статьи',
                             validators=[ MinLengthValidator(5, message="Минимум 5 символов"),
                                          MaxLengthValidator(100, message="Максимум 100 символов"),])

    anouncement = models.CharField(max_length=300, default='', verbose_name='Аннотация',
                                   validators=[ MinLengthValidator(5, message="Минимум 5 символов"),
                                                MaxLengthValidator(100, message="Максимум 300 символов"),])
    text = models.TextField(default='', verbose_name='Текст', validators=[ MinLengthValidator(5, message="Минимум 5 символов"),])


    date = models.DateTimeField( verbose_name='Дата написания', null=False, auto_now_add=True ) #  auto_created=True, auto_now_add=True,   default=timezone.now,
    category = models.CharField(choices=categories, max_length=20, verbose_name='Категория')
    tags = models.ManyToManyField(to=Tag, blank=True)

    def __str__(self):
        return f"{self.title[0:16]} / {self.text[0:128]}{'...'} Автор- {str(self.author)}"

    def image_tag(self):
        image = Image.objects.filter(article=self)
        if image:
            return mark_safe (f'<img src="{image[0].image.url}" width="auto" height="50"/>')
        else:
           return '(No image)'

    def get_absolute_url(self):
        return f'/news/{self.id}/'

    def get_views(self):
        return self.views.count()

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Image (models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, blank=True)
    image = models.ImageField(upload_to='article_images/', verbose_name='Иллюстрации', blank=True)

    def ___str__(self):
        return self.title

    def image_tag(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="50"/>')
        #image = Image.objects.filter(article=self)
        #print('!!!!', image)
        # if image:
        #     return mark_safe(f'<img src="{image[0].image.url}" height="50px" width="auto" />')
        # else:
        #     return '(no image)'

    class Meta:
        verbose_name = 'Иллюстрация'
        verbose_name_plural = 'Иллюстрации'


class ViewCount(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE,
                                related_name='views')
    ip_address = models.GenericIPAddressField()
    view_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-view_date',)
        indexes = [models.Index(fields=['-view_date'])]

    def __str__(self):
        return self.article.title


