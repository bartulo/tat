from django import template
register = template.Library()

@register.filter(name='addph')
def addph(field, css):
   return field.as_widget(attrs={"class":"form-control", "placeholder": css})

@register.filter(name='quitarcom')
def quitarcom(obj):
    return obj.replace('"','')
