from django import  template

register = template.Library()


@register.simple_tag
def percent(num1,num2):
    try:
        s = str(round(num1/num2,1)*100) + "%"
    except Exception:
        s = "-"
    return s