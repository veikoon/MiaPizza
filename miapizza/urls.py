from django.urls import path

from . import views


app_name = 'miapizza'
urlpatterns = [
    path('', views.IndexView, name='base'),
    path('login/', views.LoginView, name='login'),
    path('ingredients/', views.IngredientView, name='ingredients'),
    path('pizzas/', views.PizzaView, name='pizzas'),
    path('remove/', views.remove, name='remove'),
    path('add/', views.add, name='add'),
    path('removePizza/', views.removePizza, name='removePizza'),
    path('addPizza/', views.addPizza, name='addPizza'),
]

