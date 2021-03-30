from django import template
from django.contrib.auth.models import Group


register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    """Check if users in the Doctors group."""
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False
