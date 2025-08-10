import importlib
import inspect

from django import template
from django.apps import apps
from django.forms import widgets

register = template.Library()

def auto_register_widget_tags():
    for app_config in apps.get_app_configs():
        if app_config.name.startswith('django.') or app_config.name == 'config':
            continue

        try:
            widgets_module = importlib.import_module(f'{app_config.name}.widgets')

            for name in dir(widgets_module):
                obj = getattr(widgets_module, name)

                if (inspect.isclass(obj) and
                    issubclass(obj, widgets.Widget) and
                    obj is not widgets.Widget and
                    hasattr(obj, 'get_template_tag') and
                    inspect.isfunction(getattr(obj, 'get_template_tag'))
                   ):
                    try:
                        widget_instance = obj()

                        raw_tag_callable = obj.get_template_tag()

                        def wrapped_tag_callable(context, *args, **kwargs):
                            return raw_tag_callable(widget_instance, context, *args, **kwargs)

                        tag_name = getattr(raw_tag_callable, '_tag_name', None)
                        takes_context = getattr(raw_tag_callable, '_takes_context', False)
                        is_simple_tag = getattr(raw_tag_callable, '_is_simple_tag', False)
                        is_filter = getattr(raw_tag_callable, '_is_filter', False)
                        doc = getattr(raw_tag_callable, '__doc__', '')

                        if raw_tag_callable and tag_name:
                            if is_simple_tag:
                                register.simple_tag(wrapped_tag_callable, name=tag_name, takes_context=takes_context)
                            elif is_filter:
                                register.filter(wrapped_tag_callable, name=tag_name)
                            else:
                                print(f"Warning: {app_config.name}.{obj.__name__} returned an unrecognized tag type or missing metadata.")
                            wrapped_tag_callable.__doc__ = doc
                        else:
                            print(f"Warning: {app_config.name}.{obj.__name__}.get_template_tag did not provide valid metadata.")

                    except Exception as e:
                        print(f"Error processing widget {obj.__name__} in {app_config.name}: {e}")

        except ImportError:
            pass
        except Exception as e:
            print(f"Error during module import or iteration in {app_config.name}: {e}")

@register.filter
def get_attr(obj, attr_string):
    parts = attr_string.split('.')
    current_obj = obj
    for part in parts:
        try:
            current_obj = getattr(current_obj, part)
        except AttributeError:
            return None
    return current_obj

def get_widget_urls():
    urls = []

    for app_config in apps.get_app_configs():
        try:
            widgets_module = importlib.import_module(f'{app_config.name}.widgets')

            for name in dir(widgets_module):
                obj = getattr(widgets_module, name)

                if (inspect.isclass(obj) and
                    issubclass(obj, widgets.Widget) and
                    obj is not widgets.Widget and
                    hasattr(obj, 'get_template_tag') and
                    inspect.isfunction(getattr(obj, 'get_template_tag'))
                   ):
                    try:
                        widget_instance = obj()
                        urls.extend(widget_instance.get_urls())

                    except Exception as e:
                        print(f"Error processing widget {obj.__name__} in {app_config.name}: {e}")

        except ImportError:
            pass
        except Exception as e:
            print(f"Error during module import or iteration in {app_config.name}: {e}")

    return urls
