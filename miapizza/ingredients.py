import datetime
import json


from django.db import models
from django.utils import timezone


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    last_update = models.DateTimeField('Dernier mouvement')
    quentity = models.IntegerField(default=0)
    def __str__(self):
        return self.name
        
class History(models.Model):
    message = models.CharField(max_length=200, null=True)
    style = models.CharField(max_length=200, null=True)

class Pizza(models.Model):
    name = models.CharField(max_length=200, null=True)
    ingredients = models.CharField(max_length=500)
    last_update = models.DateTimeField('Dernier mouvement')
    def set_ingredients(self, list):
        self.ingredients = json.dumps(list)
    def get_ingredients(self):
        return json.loads(self.ingredients)
    def __str__(self):
        return self.name
