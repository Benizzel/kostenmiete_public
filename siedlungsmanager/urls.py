from django.urls import path
from .views import SiedlungHome
from .views import SiedlungCreate, ObjektCreate
from .views import SiedlungDetail
from .views import SiedlungUpdate
from .views import SiedlungDelete
from .views import ObjektDetail

urlpatterns = [
    # .as_view() because Siedlung_Home is a class
    # name is the name of the url. So we can access the url by name from 0 everywhere
    path('', SiedlungHome.as_view(), name='siedlung_home'),
    path('create-siedlung/', SiedlungCreate.as_view(), name='siedlung_create'),
    # Needs a call with the pk of the object like {% url 'siedlung_detail' siedlung.pk}
    path('<int:pk>/', SiedlungDetail.as_view(), name='siedlung_detail'),
    path('<int:pk>/update/', SiedlungUpdate.as_view(), name='siedlung_update'),
    path('<int:pk>/delete/', SiedlungDelete.as_view(), name='siedlung_delete'),
    path('<int:pk>/create-objekt/', ObjektCreate.as_view(), name='objekt_create'),
    path('<int:pk>/detail-objekt', ObjektDetail.as_view(), name='objekt_detail')
]


