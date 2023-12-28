from django.urls import path
from users import views

urlpatterns = [
    path('', views.registration, name='registration'),
    path('account/', views.profile_update, name = 'account' ),
    path('account1/<int:pk>', views.AccountUpdateView.as_view(), name='account1')

]