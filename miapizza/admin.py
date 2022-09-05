from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

from .models import Ingredient, Pizza

class IngredientAdmin(ImportExportModelAdmin): # used to allow import/export from admin panel.
    pass

class PizzaAdmin(ImportExportModelAdmin): # used to allow import/export from admin panel.
    pass
    
admin.site.register(Ingredient, IngredientAdmin)

admin.site.register(Pizza, PizzaAdmin)
