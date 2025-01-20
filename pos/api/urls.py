from django.urls import path, include
from api import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import TableUserListApiView, TableUserDetailApiView,TableOrderListApiView, TableOrderDetailApiView, RegisterView, LoginView, LogoutView

app_name = 'api'

urlpatterns = [
    path('api/table_user', views.TableUserListApiView.as_view()),
    path('api/table_user/<int:id>', views.TableUserDetailApiView.as_view()),
    path('api/table_order', views.TableOrderListApiView.as_view()),
    path('api/table_order/<int:id>', views.TableOrderDetailApiView.as_view()),
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]