from import_export import resources
from .models import Ingredient, Pizza

class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient

class PizzaResource(resources.ModelResource):
    class Meta:
        model = Pizza