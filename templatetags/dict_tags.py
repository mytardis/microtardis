from django import template
register = template.Library()

def dict_get(dict, key):
    #custom template tag used like so:
    #{{dictionary|dict_get:var}}
    #where dictionary is duh a dictionary and var is a variable representing
    #one of it's keys
    try:
        value = dict[key]
    except KeyError:
        return ""
    return value

register.filter('dict_get',dict_get)
