

import sys
from abc import ABCMeta, abstractmethod, abstractproperty
from collections import Sequence, Mapping
from types import ClassType

NOT_RECOMMENDED = type('NotRecommended', (), {})()


# class Interface(metaclass=ABCMeta):
#   pass
class Interface:
  __metaclass__ = ABCMeta
  @abstractmethod
  def __init__(self):
    raise NotImplementedError('call to interface constructor')

class Abstract:
  __metaclass__ = ABCMeta
  @abstractmethod
  def __init__(self):
    raise NotImplementedError('call to abstract constructor')


def to_dict(thing, default_value=None):
  if isinstance(thing, str):
    thing = tuple(name for name in (name.strip() \
        for name in thing.split(',')) if name)
  if isinstance(thing, Sequence):
    dict_thing = dict((name, default_value) \
        for name in thing)
  elif isinstance(thing, Mapping):
    dict_thing = dict((name, default_value if value is None else value) \
        for (name, value) in thing.items)
  else:
    raise TypeError('invalid thing(first argument), expected a string sequence '
        + 'or mapping but found {:s}'.format(type(thing).__name__))
  return dict_thing


def create_abstract_property(name, fget=True, fset=False, fdel=False, doc=None):
  prop = abstractproperty(
      fget if callable(fget) else (lambda self: None) if fget else None,
      fset if callable(fset) else (lambda self: None) if fset else None,
      fdel if callable(fdel) else (lambda self: None) if fdel else None,
      doc)
  prop.__name__ = name
  return prop


def create_abstract_method(name, method, doc=None):
  meth = abstractmethod(method)
  meth.__name__ = name
  if doc is not None: meth.__doc__ = doc
  return meth


def create_abstract_class(abstract_class_name, properties, methods
    , base_classes=object, mixins={}, __init__=None):
  if isinstance(base_classes, type) or isinstance(base_classes, ClassType):
    base_classes = (base_classes,)
  def not_implemented(self, *args, **kwargs):
    raise NotImplementedError('call to abstract method')
  abstract_properties = dict((name, create_abstract_property(name, *args)) \
    for (name, args) in to_dict(properties, (not_implemented,)).items())
  abstract_methods = dict((name, create_abstract_method(name, *args)) \
      for (name, args) in to_dict(methods, (not_implemented,)).items())
  if __init__:
    abstract_methods['__init__'] = create_abstract_method('__init__', __init__ \
        if callable(__init__) else not_implemented)
  mixins = dict(mixins)
  mixins.update(abstract_properties)
  mixins.update(abstract_methods)
  mixins['__metaclass__'] = ABCMeta
  return type(abstract_class_name, base_classes, mixins)


def create_proxy_class(proxy_class_name, target_class, proxy_attr_name
    , source_class, source_method_names):
  if proxy_class_name is NOT_RECOMMENDED:
    TargetClass = target_class
  else:
    class TargetClass(target_class):
      def __init__(self, *args, **kwargs):
        setattr(self, proxy_attr_name, source_class())
        super(self.__class__, self).__init__(*args, **kwargs)
    setattr(TargetClass, proxy_attr_name, None)
    TargetClass.__name__ = proxy_class_name
  if type(source_method_names) is str:
    source_method_names = tuple(name.strip() for name in (name.strip()
        for name in source_method_names.split(',')) if name)
  if isinstance(source_method_names, Sequence):
    source_method_names = dict((name, name) for name in source_method_names)
  elif not isinstance(source_method_names, Mapping):
    raise TypeError('method names (optional third argument expects a comma '
        + ' seperated string, list or mapping, but found type {:s}'
        .format(repr(source_method_names)))
  for (name, proxy_name) in source_method_names.items():
    define_proxy_method(TargetClass, source_class, proxy_attr_name
        , name, proxy_name)
  return TargetClass


def define_proxy_method(target_class, source_class, proxy_attr_name
    , source_method_name, proxy_method_name=None):
  if proxy_method_name is None:
    proxy_method_name = source_method_name
  source_class_name = source_class.__name__
  source_method = getattr(source_class, source_method_name)
  if callable(source_method):
    if isinstance(source_method, staticmethod):
      proxy_method = staticmethod(lambda *args, **kwargs: \
          source_method(*args, **kwargs))
    elif isinstance(source_method, classmethod):
      proxy_method = classmethod(lambda cls, *args, **kwargs: \
          source_method(source_class, *args, **kwargs))
    else:    # isinstance(source_method, instancemethod)
      #print(target_class, proxy_attr_name, proxy_method_name)
      proxy_method = lambda self, *args, **kwargs: getattr(getattr(self, proxy_attr_name), source_method_name)(*args, **kwargs)
      #getattr(getattr(health, '_feeling_proxy'), 'question')()
    proxy_method.__name__ = proxy_method_name
    proxy_method.__doc__ = source_method.__doc__
    setattr(target_class, proxy_method_name, proxy_method)
  elif isinstance(source_method, property):   # attribute method
    proxy_getter = source_method.fget and (lambda self: getattr(getattr(self, proxy_attr_name), source_method_name))
    proxy_setter = source_method.fset and (lambda self, value: setattr(getattr(self, proxy_attr_name), source_method_name, value))
    proxy_deleter = source_method.fdel and (lambda self: delattr(getattr(self, proxy_attr_name), source_method_name))
    proxy_method = property(proxy_getter, proxy_setter, proxy_deleter \
        , source_method.__doc__)
    setattr(target_class, proxy_method_name, proxy_method)
  else:   # attribute variable
    proxy_getter = (lambda self: getattr(getattr(self, proxy_attr_name), source_method_name))
    proxy_setter = (lambda self, value: setattr(getattr(self, proxy_attr_name), source_method_name, value))
    proxy_deleter = (lambda self: delattr(getattr(self, proxy_attr_name), source_method_name))
    proxy_method = property(proxy_getter, proxy_setter, proxy_deleter \
        , source_method.__doc__)
    setattr(target_class, proxy_method_name, proxy_method)


def sanity_test():
  class Health(object):
    pass

  class Feeling(object):
    _feeling = None
    def __init__(self, feeling='uncertain'):
      self._feeling = feeling
    
    @property
    def feeling(self): return self._feeling
    
    @feeling.setter
    def feeling(self, feeling): self._feeling = feeling
    
    def question(self, who=None):
      if who is None:
        return 'Are you feeling {:s}?'.format(self._feeling)
      return 'Is {:s} feeling {:s}?'.format(who, self._feeling)
    
    def answer(self, who=None):
      if who is None:
        return 'I\'m feeling {:s}.'.format(self._feeling)
      return '{:s} is feeling {:s}.'.format(who, self._feeling)
  
  
  ProxyHealth = create_proxy_class('ProxyHealth', Health, '_feeling_proxy' \
      , Feeling, '_feeling,feeling,question,answer')
  
  h = ProxyHealth()
  assert h.feeling == 'uncertain'
  h.feeling = 'happy'
  assert h.feeling == 'happy'
  assert h.question() == 'Are you feeling happy?'
  assert h._feeling_proxy._feeling == 'happy'
  assert h._feeling == 'happy'
  h._feeling = 'sad'
  assert h.feeling == 'sad'
  assert h.question() == 'Are you feeling sad?'
  assert h.question('Lia') == 'Is Lia feeling sad?'


sanity_test()
