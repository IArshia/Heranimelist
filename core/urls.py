from django.urls import path
from django.views.generic import TemplateView
from .import views

urlpatterns = [
    path('', TemplateView.as_view(template_name='core/index.html'), name='home'),
    path('signup/', views.RegisterView.as_view(), name='signup'),
]
