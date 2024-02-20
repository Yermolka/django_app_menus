from django.db import models

class Menu(models.Model):
    menu_name = models.CharField(max_length=50)

class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=50)
    item_parent = models.CharField(max_length=50)
    item_relative_url = models.CharField(max_length=50)
