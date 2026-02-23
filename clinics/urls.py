from django.urls import path , include
from rest_framework.routers import DefaultRouter
from .views import DistrictViewSet, CountyViewSet, SubcountyViewSet, ParishViewSet, VillageViewSet
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'clinics'

router = DefaultRouter()
router.register(r'districts', DistrictViewSet, basename='district')
router.register(r'counties', CountyViewSet, basename='county')
router.register(r'subcounties', SubcountyViewSet, basename='subcounty')
router.register(r'parishes', ParishViewSet, basename='parish')
router.register(r'villages', VillageViewSet, basename='village')

urlpatterns = [  # list all clinics
    path('create/', views.clinic_create, name='clinic_create'),
    path('<int:pk>/dashboard/',views.clinic_dashboard_view, name = 'dashboard'),
    path('<int:pk>/', views.clinic_detail, name='clinic_detail'),
    path('<int:pk>/edit/', views.clinic_edit, name='clinic_edit'),
    path('<int:pk>/delete/', views.clinic_delete, name='clinic_delete'),

    # api
    path('api/', include(router.urls), name='apis'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)