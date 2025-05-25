from django import template
from menu.models import Menu
from django.urls import resolve

register = template.Library()

@register.inclusion_tag('menu/menu.html', takes_context=True)
def draw_menu(context, menu_name):
    request = context['request']
    try:
        menu = Menu.objects.get(name=menu_name)
    except Menu.DoesNotExist:
        return {'menu_items': [], 'open_items': set(), 'current_url': request.path}

    items = list(menu.items.select_related('parent').all())
    tree = build_tree(items)
    open_items = find_open_path(tree, request.path)

    return {
        'menu_items': tree,
        'open_items': open_items,
        'current_url': request.path,
    }

def build_tree(items):
    lookup = {}
    for item in items:
        # создаём своё поле для вложенных
        setattr(item, 'children_items', [])
        lookup[item.id] = item

    tree = []
    for item in items:
        if item.parent_id:
            parent = lookup.get(item.parent_id)
            if parent:
                parent.children_items.append(item)
        else:
            tree.append(item)
    return tree

def find_open_path(tree, current_url):
    open_set = set()
    def dfs(item, path):
        url = item.get_absolute_url()
        if url == current_url:
            # отмечаем все узлы в пути + сам найденный
            open_set.update(p.id for p in path)
            open_set.add(item.id)
            return True
        for child in getattr(item, 'children_items', []):
            if dfs(child, path + [item]):
                return True
        return False

    for root in tree:
        dfs(root, [])
    return open_set
