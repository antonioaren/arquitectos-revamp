from django import template

register = template.Library()


@register.inclusion_tag("header/menu.html", takes_context=True)
def menu(context):
    return {
        "request": context["request"],
        "name": "hola soy soy templatetags",
    }
