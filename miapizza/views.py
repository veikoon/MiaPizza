from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
import difflib

from .models import Ingredient, Pizza, History
from . import forms

@login_required
def IndexView(request):
    template_name = 'miapizza/base.html'
    return render(request, template_name)

def LoginView(request):
    template_name = 'miapizza/login.html'
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('miapizza:base')
            else:
                message = 'Login failed!'
    context = {'form': form, 'message': message}
    return render(request, template_name, context)

@login_required
def IngredientView(request):
    template_name = 'miapizza/ingredients.html'
    ingredients = Ingredient.objects.order_by('name')[:]
    last_history = {}
    if History.objects.exists():
        last_history = {
        'message' : History.objects.last().message,
        'style' : History.objects.last().style,
        }
        History.objects.last().delete()
    context = {
        'ingredients_list': ingredients,
        'last_history': last_history
    }
    return render(request, template_name, context)

@login_required
def PizzaView(request):
    template_name = 'miapizza/pizzas.html'
    pizzas = Pizza.objects.order_by('name')[:]
    last_history = {}
    if History.objects.exists():
        last_history = {
        'message' : History.objects.last().message,
        'style' : History.objects.last().style,
        }
        History.objects.last().delete()
    context = {
        'pizzas_list': pizzas,
        'last_history': last_history
    }
    return render(request, template_name, context)

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
        #object = get_object_or_404(Ingredient, name=ingredient)
        try:
            object = Ingredient.objects.get(name=ingredient) 
        except:
            ingredients_list = [ingre.name for ingre in Ingredient.objects.all()]
            most_accurate = difflib.get_close_matches(ingredient, ingredients_list, 1)
            error_message = "Error ingrédient \"" + ingredient + "\" introuvable !"
            if len(most_accurate) >= 1:
                error_message += " Vouliez vous écrire : \"" + most_accurate[0] + "\" ?"
            History.objects.get_or_create( #get if user uses back button
                message = error_message,
                style = "danger"
            )
            return
        change(object, str(ingredients[ingredient] * int(number)), sign)
    historique(pizza, number, sign)
    

def removePizza(request):
    changePizza(request, -1)
    return HttpResponseRedirect(reverse('miapizza:pizzas'))

def addPizza(request):
    changePizza(request, 1)
    return HttpResponseRedirect(reverse('miapizza:pizzas'))