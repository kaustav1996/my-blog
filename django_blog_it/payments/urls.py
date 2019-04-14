from . import views
from django.conf.urls import url


urlpatterns = [
    url('', views.PaymentPage.as_view(), name='payments'),
    url('^charge/', views.charge, name='charge'),
]