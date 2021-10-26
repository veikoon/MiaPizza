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

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

def change(object, number, sign):
    if number == '': # If the string is empty, put 1 into the string
        number = '1'
    if check_int(number): # Check if the string is an int
        object.quentity += abs(int(number)) * sign
        object.last_update = timezone.now()
        object.save()
        f= open("data/logs.txt","a")
        f.write(str(object.last_update.strftime("%Y-%m-%d %H:%M:%S"))
            + " "
            + str(object.name)
            + " : " 
            + str(number * sign)
            + " donc total de "
            + str(object.quentity)
            + "\n")
        f.close()
        if int(number) * sign <0:
            style_alert = "warning"
        else:
            style_alert = "success"
        History.objects.get_or_create( #get if user uses back button
            message = (
                str(number * sign)
                + " pour l'ingredient "
                + str(object.name)
                + str(object.last_update.strftime(" à %H:%M:%S."))
            ),
            style = style_alert
        )
    else: # Ask to give an int
        History.objects.get_or_create( #get if user uses back button
            message = "Merci de rentrer un nombre valide", style = "danger"
        )

    
def remove(request):
    ingredients = get_object_or_404(Ingredient, pk=request.POST['id']) 
    number = request.POST['num']
    change(ingredients, number, -1)
    return HttpResponseRedirect(reverse('miapizza:base'))

def add(request):
    ingredients = get_object_or_404(Ingredient, pk=request.POST['id']) 
    number = request.POST['num']
    change(ingredients, number, 1)
    return HttpResponseRedirect(reverse('miapizza:base'))

def removePizza(request):
    pizza = get_object_or_404(Pizza, pk=request.POST['id'])
    number = request.POST['num']
    ingredients = pizza.get_ingredients()
    if number == '':
        number = '1'
    if not check_int(number):
        History.objects.get_or_create( #get if user uses back button
            message = "Merci de rentrer un nombre valide", style = "danger"
        )
    else:
        for ingredient in list(ingredients):
            object = get_object_or_404(Ingredient, name=ingredient)
            change(object, str(ingredients[ingredient] * int(number)), -1)
    return HttpResponseRedirect(reverse('miapizza:base'))

def addPizza(request):
    pizza = get_object_or_404(Pizza, pk=request.POST['id'])
    number = request.POST['num']
    ingredients = pizza.get_ingredients()
    if number == '':
        number = '1'
    if not check_int(number):
        History.objects.get_or_create( #get if user uses back button
            message = "Merci de rentrer un nombre valide", style = "danger"
        )
    else:
        for ingredient in list(ingredients):
            object = get_object_or_404(Ingredient, name=ingredient)
            change(object, str(ingredients[ingredient] * int(number)), 1)
    return HttpResponseRedirect(reverse('miapizza:base'))