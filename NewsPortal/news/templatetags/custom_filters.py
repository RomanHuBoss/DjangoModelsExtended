from django import template

register = template.Library()

class CensorException(Exception):
   pass

FILTERED_WORDS = [
   'lorem',
   'ipsum',
   'dolor',
   'curabitur',
   'adipiscing',
   'fermentum'
]

@register.filter(name='censor')
def censor(value):
   try:
      if not isinstance(value, str):
         raise CensorException("Error: is not a text")

      for word in FILTERED_WORDS:
         if word in value:
            value = value.replace(word, word[:1] + '*'*(len(word)-1))
         if word.capitalize() in value:
            value = value.replace(word.capitalize(), word.capitalize()[:1] + '*'*(len(word)-1))
      return value
   except CensorException as e:
      print (e)
