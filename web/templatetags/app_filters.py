from django import template
register = template.Library()

@register.filter(name='addph')
def addph(field, css):
   return field.as_widget(attrs={"class":"form-control", "placeholder": css})

@register.filter(name='sumahoras')
def sumahoras(value):
   suma = 0
   for i in value:
      suma = suma + i.horas
   return "%.2f" % suma

@register.filter(name='horasadmin')
def admin(obj):
   total = 0
   for n in obj.admin_set.all():
      total = total + sum([r.horas for r in n.adminind_set.all()])/n.user.count()
   return "%.2f" % total

@register.filter(name='quitarcom')
def quitarcom(obj):
    return obj.replace('"','')
