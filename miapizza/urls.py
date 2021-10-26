from django.urls import path

from . import views


app_name = 'miapizza'
urlpatterns = [
    path('', views.IndexView.as_view(), name='base'),
    path('ingredients/', views.IngredientView.as_view(), name='ingredients'),
    path('pizzas/', views.PizzaView.as_view(), name='pizzas'),
    path('remove/', views.remove, name='remove'),
    path('add/', views.add, name='add'),
    path('removePizza/', views.removePizza, name='removePizza'),
    path('addPizza/', views.addPizza, name='addPizza'),
]

