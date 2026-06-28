from django.urls import path
from .views import *


urlpatterns = [
    path('csrf/',csrf_api),
    path('register/',register_api),
    path('login/',login_api),
    path('logout/',logout_api),
    path('check_auth/',check_auth_api),
    path('create/',create_short_url),
    path('my_urls/',my_urls_api),
    path('<str:short_code>',redirect_original_page),
    # path('change_password/',change_password),
]