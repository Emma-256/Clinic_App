from django.urls import path, include
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

urlpatterns = [
    path('create/', views.clinic_create, name='clinic_create'),

    # ── IMPORTANT: more-specific paths MUST come before <int:pk>/ ──────────
    # If <int:pk>/ is listed first it swallows everything beneath it,
    # including /1/inventory/add/, /1/dashboard/, /1/edit/ etc.

    path('<int:pk>/dashboard/', views.clinic_dashboard_view, name='clinic_dashboard'),
    path('<int:pk>/edit/',      views.clinic_edit,            name='clinic_edit'),
    path('<int:pk>/delete/',    views.clinic_delete,          name='clinic_delete'),

    # inventory — must be before the bare <int:pk>/ catch-all
    path('<int:clinic_pk>/inventory/', include('inventory.urls', namespace='inventory')),

    # bare detail — keep LAST among <int:pk>/... patterns
    path('<int:pk>/',           views.clinic_detail,          name='clinic_detail'),

    # api
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)