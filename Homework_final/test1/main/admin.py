from django.contrib import admin
from .models import Article, Tag, Account, Image, ViewCount
from django.db.models.functions import Length
from django.db.models import Count


# Register your models here.

class ArticleFilter(admin.SimpleListFilter):
    title = 'По длине новости'
    parameter_name = 'text'

    def lookups(self, request, model_admin):
        return [('S',("Короткие, <100 зн.")),
                ('M',("Средние, 100-500 зн.")),
                ('L',("Длинные, >500 зн.")),]

    def queryset(self, request, queryset):
        if self.value() == 'S':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=100)
        elif self.value() == 'M':
            return queryset.annotate(text_len=Length('text')).filter(text_len__lt=500,
                                                                     text_len__gte=100)
        elif self.value() == 'L':
            return queryset.annotate(text_len=Length('text')).filter(text_len__gt=500)

class ArticleImageInline(admin.TabularInline):
    model = Image
    extra = 3
    readonly_fields = ('id','image_tag')



class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date', 'category', 'symbols_count',
                    'image_tag2']  # отображаемые поля в админ панели
    #list_filter = ['title', 'author', 'date', 'category']  # поля по которым можно фильтровать модель
    list_filter = ['date', ArticleFilter ]
    list_display_links = ('title', 'author')  # поля к которым прикручиваются ссылки
    search_fields = ['title__startswith']
    ordering = ['date', 'title']  # поля по которым происходит изначальная сортировка
    list_per_page = 10  # количество отображаемых сущностей в админ панели ( пагинация )
    inlines = [ArticleImageInline, ]


    @admin.display(description='Длина', ordering='_symbols')
 #   @admin.display(description='Длина', ordering='text')
    def symbols_count(self, article: Article):
        return f"Количество символов {len(article.text)}"

    def get_queryset(self, request): # настройка сортировки по новому полю 
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(_symbols=Length('text'))
        return queryset

    @admin.display(description='Иллюстрация')  # меняем отображенение на админ панели
    def image_tag2(self, article: Article):
        return article.image_tag()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title','status','tag_count']
    list_filter = ['title','status']
    actions = ['set_true']

    @admin.display(description='Использований', ordering='tag_count')
    def tag_count(self, tag: Tag):
        return tag.tag_count

    def get_queryset(self, request):  # настройка сортировки по новому полю
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(tag_count=Count('article'))
        return queryset


class ImageAdmin(admin.ModelAdmin):
    list_filter = ['title', 'id']
    list_display = ['title', 'id', 'image_tag']


@admin.register(ViewCount)
class ViewCountAdmin(admin.ModelAdmin):
    list_display = ['article','ip_address','view_date']


admin.site.register(Image, ImageAdmin)
admin.site.register(Article, ArticleAdmin)

# admin.site.register ( Article)
#admin.site.register(Tag)
