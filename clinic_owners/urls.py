# clinic_owners/urls.py
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views
from .views import CustomLoginView

app_name = 'clinic_owners'

from django.urls import path,include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Login
    path('login/', CustomLoginView.as_view(), name='login'),
    # Owner dashboard
    path('', views.dashboard_view, name='dashboard'),
    # Owner registration
    path('register/', views.register, name='register'),
    # Profile display
    path('profile/', views.profile_view, name='profile'),
    # Profile update
    path('profile/update/', views.update_profile_view, name='update_profile'),
    # User update
    path('user/update/', views.update_user_view, name='update_user'),
    # Profile delete
    path('profile/delete/', views.delete_profile_view, name='delete_profile'),
    # Log out
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('clinics,', include('clinics.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
