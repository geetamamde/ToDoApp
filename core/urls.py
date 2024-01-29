
from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login),
    path('signup',views.signup),
    path('',views.home),
    path('signout',views.signout),
    path('addtodo',views.addtodo),
    path('delete-todo/<int:id>',views.deletetodo),
    path('change-status/<int:id>/<str:status>' ,views.changetodo ),
    path('search',views.search),

]