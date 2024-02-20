from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import MenuItem, Menu

# item_name - активный пункт меню

def index(request, item_name):
    template = loader.get_template('menus/index.html')
    context = {
        'request_path': request.path,
    }
    return HttpResponse(template.render(context, request))

def draw_menu(menu_name):
    pass