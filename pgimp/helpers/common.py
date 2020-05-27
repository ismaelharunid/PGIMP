
from collections import Sequence, Iterable


isproperty = lambda attr: not (not attr.__name__ \
    or attr.__name__.startswith('_') \
    or callable(attr) or isinstance(attr, property) )

ispropertyof = lambda obj, name: getattr(obj, name) \
    and isproperty(getattr(obj, name))

ismethod = lambda attr: not (not attr.__name__ \
    or attr.__name__.startswith('_') \
    or isinstance(attr, property) ) and callable(attr)

ismethodof = lambda obj, name: getattr(obj, name) \
    and ismethod(getattr(obj, name))

iscallable = lambda attr: attr.__name__ and not attr.__name__.startswith('_') \
    and (callable(attr) or isinstance(attr, property))

iscallableof = lambda obj, name: getattr(obj, name) \
    and iscallable(getattr(obj, name))


def replacer(token, replacements, ws=None, non_alnum=None):
  replaced = []
  i, n = 0, len(token)
  while i < n:
    for (k,v) in replacements.items():
      l_k = len(k)
      if i + l_k <= n and token[i:i+l_k] == k:
        replaced.append(v)
        i += l_k
        break
    else:
      c = token[i]
      if ws is not None and c.isspace():
        if i == 0 or not token[i-1].isspace():
          replaced.append(ws)
      elif non_alnum is not None and not c.isalnum():
        replaced.append(non_alnum)
      else:
        replaced.append(c)
      i += 1
  return ''.join(replaced)


def camel2py(token):
  i, n = 0, len(token)
  pytoken, li = [token[:i]], i
  while i < n:
    c = token[i]
    if 'A' <= c and c <= 'Z':
      pytoken.append(token[li:i])
      if i > 0 and token[i-1] != '_': pytoken.append('_')
      pytoken.append(chr(ord(c) + 0x61 - 0x41))
      li = i + 1
    i += 1
  pytoken.append(token[li:])
  return ''.join(pytoken)
assert camel2py("MyClass") == 'my_class'
assert camel2py("_MyClass") == '_my_class'
assert camel2py("__MyClass") == '__my_class'
assert camel2py("__MyClass__") == '__my_class__'
assert camel2py("__MyClassM__") == '__my_class_m__'
assert camel2py("__MyClassMethod__") == '__my_class_method__'
assert camel2py("__MyClass_Method__") == '__my_class_method__'

TO_CONTANT_NAME_REPLACMENTS = \
    { "a": ''
    , 'e': ''
    , 'i': ''
    , 'o': ''
    , 'u': ''
    , 'ck': 'k'
    , 'br': 'b', 'cr': 'c', 'fr': 'f', 'gr': 'g', 'kr': 'k', 'pr': 'p', 'tr': 'p'
    , 'colorspace': '', 'color space': ''
    }
def to_contant_name(token, max_length=8, prefix='', suffix=''
    , replacements=TO_CONTANT_NAME_REPLACMENTS):
  if token.isupper(): token = token.lower()
  if len(token) > max_length:
    short_token = replacer(token, replacements, '_', '')
    if len(short_token) > len(token):
      short_token = replacer(token, {}, '_', '')
  else:
    short_token = replacer(token, {}, '_', '')
  camel_token = camel2py(short_token)
  if len(camel_token) >= max_length+3:
    camel_token = short_token.upper()
  return (prefix + camel_token + suffix).upper()

def define_constants(tokens, max_length=8, prefix='', suffix=''):
  if isinstance(tokens, str):
    tokens = tuple(token.strip() for token in tokens.strip().split(','))
  return dict((to_contant_name(token, max_length, prefix, suffix), token) for token in tokens)

def enumerate_constants(tokens, max_length=8, prefix='', suffix=''):
  if isinstance(tokens, str):
    tokens = tuple(token.strip() for token in tokens.strip().split(','))
  return dict((to_contant_name(tokens[i_tokens], max_length, prefix, suffix), i_tokens) \
      for i_tokens in range(len(tokens)))

def maskerate_constants(tokens, max_length=8, prefix='', suffix=''):
  if isinstance(tokens, str):
    tokens = tuple(token.strip() for token in tokens.strip().split(','))
  return dict((to_contant_name(tokens[i_tokens], max_length, prefix, suffix), 2**i_tokens) \
      for i_tokens in range(len(tokens)))


