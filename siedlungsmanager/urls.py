from django.urls import path
from .views import SiedlungHome
from .views import SiedlungCreate, ObjektCreate
from .views import SiedlungDetail
from .views import SiedlungUpdate
from .views import SiedlungDelete
from .views import ObjektDetail

"""
.as_view() because class-view pattern
name is the name of the url. So we can access the url by name from 0 everywhere
pk pattern: define the pk within the url with descriptive name. Some more code to define because you need to define
the get_objects method but it is way more clear.
"""
urlpatterns = [
    path('', SiedlungHome.as_view(), name='siedlung_home'),
    path('create-siedlung/', SiedlungCreate.as_view(), name='siedlung_create'),
    path('<int:siedlung_pk>/', SiedlungDetail.as_view(), name='siedlung_detail'),
    path('<int:siedlung_pk>/update/', SiedlungUpdate.as_view(), name='siedlung_update'),
    path('<int:siedlung_pk>/delete/', SiedlungDelete.as_view(), name='siedlung_delete'),
    path('<int:siedlung_pk>/create-objekt/', ObjektCreate.as_view(), name='objekt_create'),
    path('<int:siedlung_pk>/<int:objekt_pk>/', ObjektDetail.as_view(), name='objekt_detail')
]


