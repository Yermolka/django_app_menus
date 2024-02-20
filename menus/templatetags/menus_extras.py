from django import template
from django.template.context import RequestContext

register = template.Library()

# Menu name
# - item with parent=menu
#   - item2 with parent=item
#       - item4 with parent=item2
# - item3 with parent=menu
@register.inclusion_tag('menus/menus.html', takes_context=True)
def draw_menu(context: RequestContext, menu_name: str):
    from ..models import MenuItem
    res = MenuItem.objects.filter(menu__menu_name = menu_name)[:]
    path = context['request_path'].rstrip('/')

    output = {'results': res, 
            'menu_name': menu_name, 
            'request_path': path,
            'depth_reached': path == '',
            'open_items': []}

    if path == '' or not res:
        return output
    
    # Find the item with current URL
    open_items = []
    cur = None
    for item in res:
        if item.item_relative_url == path:
            cur = item    
            open_items.append(item)
            break

    if cur is None:
        return output

    # Find all higher items that should be rendered open
    while cur.item_parent != 'menu':
        for item in res:
            if item.item_name == cur.item_parent:
                cur = item
                open_items.append(item)
                break
    
    output['open_items'] = open_items
    return output


@register.inclusion_tag('menus/menu_items.html', takes_context=True)
def draw_menu_items(context: RequestContext, root_name: str, items: list):
    path = context.get('request_path')
    if len(items) == 0:
        return {'results': [], 'others': []}
    
    res = get_children(root_name, items)

    output = {
        'results': res[0], 
        'others': res[1], 
        'request_path': path,
        'open_items': context.get('open_items')
        }
    
    return output

# Return item's children in res, all other elements in leftover
@register.simple_tag
def get_children(root_name: str, items: list):
    res = []
    leftover = []
    for i in items:
        if i.item_parent == root_name:
            res.append(i)
        else:
            leftover.append(i)
    return res, leftover