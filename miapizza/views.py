from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime


from .ingredients import Ingredient, Pizza
from .ingredients import History

class IndexView(generic.TemplateView):
    template_name = 'miapizza/base.html'
    
class IngredientView(generic.ListView):
    model = Ingredient
    template_name = 'miapizza/ingredients.html'
    context_object_name = 'ingredients_list'
    def get_queryset(self):
        return Ingredient.objects.order_by('name')[:]
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if History.objects.exists():
            context['last_history'] = {
            'message' : History.objects.last().message,
            'style' : History.objects.last().style,
            }
            History.objects.last().delete()
        return context

class PizzaView(generic.ListView):
    model = Pizza
    template_name = 'miapizza/pizzas.html'
    context_object_name = 'pizzas_list'
    def get_queryset(self):
        return Pizza.objects.order_by('name')[:]
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        if History.objects.exists():
            context['last_history'] = {
            'message' : History.objects.last().message,
            'style' : History.objects.last().style,
            }
            History.objects.last().delete()
        return context

def change(ingredient, number, sign):
    ingredient.quentity += abs(int(number)) * sign
    ingredient.last_update = timezone.now()
    ingredient.save()
    log(ingredient, number, sign)
    

def log(ingredient, number, sign):
    f= open("data/logs.txt","a")
    f.write(str(ingredient.last_update.strftime("%Y-%m-%d %H:%M:%S"))
        + " "
        + str(ingredient.name)
        + " : " 
        + str(number * sign)
        + " donc total de "
        + str(ingredient.quentity)
        + "\n")
    f.close()

def historique(object, number, sign):
    signe = ''
    if int(number) * sign <0:
        style_alert = "warning"
    else:
        style_alert = "success"
        signe = '+'
    History.objects.get_or_create( #get if user uses back button
        message = (
            "Stock actualisé de "
            + signe
            + str(int(number) * sign)
            + " "
            + str(object.name)
            + str(object.last_update.strftime(" à %H:%M:%S."))
        ),
        style = style_alert
    )
    
def changeIngredient(request, sign):
    ingredient = get_object_or_404(Ingredient, pk=request.POST['id']) 
    number = request.POST['num']
    if ingredient.unit == Ingredient.Unites.gramme and sign == 1 and int(number) < 500:
        History.objects.get_or_create( #get if user uses back button
            message = "Impossible d'ajouter une valeur inférieur à 500 !",
            style = "danger"
        )
        return
    if number == '':
        number = '1'
    change(ingredient, number, sign)
    historique(ingredient, number, sign)
    
    
def remove(request):
    changeIngredient(request, -1)
    return HttpResponseRedirect(reverse('miapizza:ingredients'))

def add(request):
    changeIngredient(request, 1)
    return HttpResponseRedirect(reverse('miapizza:ingredients'))

def changePizza(request, sign):
    pizza = get_object_or_404(Pizza, pk=request.POST['id'])
    number = request.POST['num']
    ingredients = pizza.get_ingredients()
    if number == '':
        number = '1'
    for ingredient in list(ingredients):
        object = get_object_or_404(Ingredient, name=ingredient)
        change(object, str(ingredients[ingredient] * int(number)), sign)
    historique(pizza, number, sign)
    

def removePizza(request):
    changePizza(request, -1)
    return HttpResponseRedirect(reverse('miapizza:pizzas'))

def addPizza(request):
    changePizza(request, 1)
    return HttpResponseRedirect(reverse('miapizza:pizzas'))