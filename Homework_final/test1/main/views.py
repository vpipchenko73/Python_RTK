from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Article, User, Account, Image
from django.db import connection
from datetime import datetime
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView  # импортируем класс получения деталей объекта
from .forms import ArticleForm_Detail, ArticleFormCreate, UserAuthForm, ArticleForm, ImagesFormSet # импортируем формы
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserChangeForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator




# главная
def index(request):
    articles_last = Article.objects.all().last()
    author_list = User.objects.all()
    account_list = Account.objects.all()
    category_list = Article.categories
    user_l=['Anonimus']
    form = UserAuthForm()


    if User.is_authenticated :
        user_l = request.user.username
        print (user_l)
    if User.is_anonymous:
        print('Anonym')
    date_time = datetime.utcnow()
    quantity_articles = Article.objects.all().count()
    quantity_user = User.objects.all().count()
    quantity_authors = User.objects.filter(groups__name='Authors').count()
    print (quantity_authors)
    context = {'articles_last': articles_last, 'author_list': author_list,'date_time': date_time,
               'quantity_articles': quantity_articles, 'quantity_user': quantity_user,'quantity_authors': quantity_authors, 'category_list': category_list,
               'user_l' : user_l, 'form':form }
    #return render(request, 'main/index.html', context)

    if request.method=='POST':
        form = UserAuthForm(request.POST)
        if form.is_valid():
        #username = request.POST.get("username")
        #password = request.POST.get("password")
        #print( username, password)
        #authenticate(username = username, password = username)
        #print (User,"*****")
        #if User.is_authenticated :
        #   print ("Юзер аутентифицирован")
        #    login(request, user)
        #else:
        #    print ("Нет такого юзера")
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user and user.is_active:
                 login(request, user)
    return render(request, 'main/index.html', context)





# калькулятор
def calc(request, a, operation, b):
    result = 0
    match operation:
        case 'plus':
            result = int(a) + int(b)
        case 'minus':
            result = int(a) + int(b)
        case 'multiply':
            result = int(a) * int(b)
        case 'divide':
            result = int(a) / int(b)
        case _:
            return HttpResponse(f" Вы ввели не верную команду")
    return HttpResponse(f" Вы ввели  A-> {a} B-> {b} <br>Операция -> {operation}  <br>Результат -> {result}")


# обработка 404
def custom_404(request, exception):
    print("ERROR")
    return HttpResponse(f"Такой страницы не существует (((")


def test(request):
    if request.method == "POST":
        print (f"Метод ->>{request.method}  Request->>{request.POST}")
        title = request.POST.get("title")
        price = float (request.POST.get("price"))
        quantiti = int(request.POST.get("quantiti"))
        new_product = Product (title, price, quantiti)
        print ( new_product )
        print (new_product.amound())

    else:
        print(f"Метод ->>{request.method}  Request->>{request.POST}")

    return render(request, 'main/news_test.html')

@login_required(login_url='index')
def news_all(request):
    #articles = Article.objects.all()
    #context = {'today_articles': articles}
    author_list = []
    author_temp = Article.objects.all().values('author', 'author__username')
    for i in author_temp: # цикл удаления из массива повторяющихся авторов
        #print(i)
        if (i in author_list) == False:
            author_list.append(i)
    account_list = Account.objects.all()
    category_list = Article.categories
    selected = 0
    if request.method == "POST":
        #print(request.POST)
        select_a = int (request.POST.get('author_filter'))
        select_c = int(request.POST.get('category_filter'))

        if select_a == 0:
            articles = Article.objects.all()
        else:
            articles = Article.objects.filter(author=select_a)
            #print(connection.queries)
        if select_c != 0:  # фильтруем найденные по авторам результаты по категориям
            articles = articles.filter(category__icontains=category_list[select_c - 1][0])
    else:
        select_a = 0
        select_c = 0
        articles = Article.objects.all()
#-------------------------------------------------------------------------------
    # сортировка от свежих к старым новостям
    articles = articles.order_by('-date')
    total = len(articles)
    p = Paginator(articles, 2)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
#------------------------------------------------------------------------------
#    context = {'articles': articles, 'author_list': author_list, 'selected': selected, 'account_list': account_list,
#               'category_list': category_list }

    context = {'articles': page_obj, 'author_list': author_list, 'selected': selected, 'account_list': account_list,
               'category_list': category_list}

    return render(request, 'main/news_all.html', context)

from .utils import ViewCountMixin

class ArticleDetailView(ViewCountMixin, DetailView):
    model = Article
    form_class = ArticleForm_Detail
    context_object_name ='article'
    template_name = 'main/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['images'] = images
        context['author_arct']=current_object.author
        return context

class ArticleCreateView(CreateView):
    template_name = 'main/news_create.html'
    form_class = ArticleFormCreate

@login_required(login_url='index')
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            if current_user.id != None: #проверили что не аноним
                new_article = form.save(commit=False)
                new_article.author = current_user
                new_article.save() #сохраняем в БД
                form.save_m2m() #сохраняем теги
                for img in request.FILES.getlist('image_field'):
                    Image.objects.create(article=new_article, image=img, title=img.name)
                print ('save ok')
                return redirect('index')
    else:
        form = ArticleForm()
    return render(request,'main/news_create1.html', {'form':form })


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = 'main/news_create2.html'
    fields = ['title','anouncement','text', 'category', 'tags']

    def get_context_data(self, **kwargs):
        context = super(ArticleUpdateView, self).get_context_data(**kwargs)
        current_object = self.object
        images = Image.objects.filter(article=current_object)
        context['image_form'] = ImagesFormSet(instance=current_object)
        return context

    def post(self, request, **kwargs):
        request.POST = request.POST
        current_object = Article.objects.get(id=request.POST['image_set-0-article'])
        deleted_ids = []
        for i in range(int(request.POST['image_set-TOTAL_FORMS'])): #удаление всех по галочкам
            field_delete =f'image_set-{i}-DELETE'
            field_image_id = f'image_set-{i}-id'
            if field_delete in request.POST and request.POST[field_delete] =='on':
                image = Image.objects.get(id=request.POST[field_image_id])
                image.delete()
                deleted_ids.append(field_image_id)

                #тут же удалить картинку из request.FILES
        #Замена картинки
        for i in range(int(request.POST['image_set-TOTAL_FORMS'])):  # удаление всех по галочкам
            field_replace = f'image_set-{i}-image' #должен быть в request.FILES
            field_image_id = f'image_set-{i}-id'  #этот файл мы заменим
            if field_replace in request.FILES and request.POST[field_image_id] != '' and field_image_id not in deleted_ids:
                image = Image.objects.get(id=request.POST[field_image_id]) #
                image.delete() #удаляем старый файл
                for img in request.FILES.getlist(field_replace): #новый добавили
                    Image.objects.create(article=current_object, image=img, title=img.name)
                del request.FILES[field_replace] #удаляем использованный файл
        if request.FILES: #Добавление нового изображения
            print('!!!!!!!!!!!!!!!!!',request.FILES)
            for input_name in request.FILES:
                for img in request.FILES.getlist(input_name):
                    print('###############',img)
                    Image.objects.create(article=current_object, image=img, title=img.name)


        return super(ArticleUpdateView, self).post(request, **kwargs)


class ArticleDeleteView(DeleteView):
    #model = Article
    queryset = Article.objects.all()
    success_url = reverse_lazy('index')  # именованная ссылка или абсолютную
    template_name = 'main/news_delete.html'


def logout_view(request):
    logout(request)
    return redirect('index')




