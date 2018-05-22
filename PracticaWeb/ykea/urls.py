from django.conf.urls import url
from django.contrib.auth.views import login, logout

from . import views

listOfAddresses = ["161.116.56.65","161.116.56.165"]

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^items/$', views.categories, name='categories'),
    url(r'^items/(?P<category>.*)/$', views.items_category, name='items_category'),
    url(r'^item/(?P<item_number>.*)/$', views.item_detail, name='item_detail'),
    url(r'^shoppingcart/$', views.shoppingcart, name='shoppingcart'),
    url(r'^buy/$', views.buy, name='buy'),
    url(r'^process/$', views.process, name='process'),
    url(r'^delete/(?P<item_number>.*)/$', views.delete, name='delete'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^accounts/login/$',  login,  name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^comparator/$', views.comparator, kwargs={'ips': listOfAddresses}, name='comparator'),
]

