from django.urls import path
from .views import SiedlungHome
from .views import SiedlungCreate

urlpatterns = [
    # .as_view() because Siedlung_Home is a class
    # name is the name of the url. So we can access the url by name from 0 everywhere
    path('', SiedlungHome.as_view(), name='siedlung_home'),
    path('create-siedlung/', SiedlungCreate.as_view(), name='siedlung_create'),
]


