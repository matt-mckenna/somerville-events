from django.urls import path
from . import views

urlpatterns = [
    path('', views.newmulti, name='newmulti'),
    path('update_data/', views.update_data, name='update_data'),
    path('add-event/', views.add_event, name='add_event'),

]