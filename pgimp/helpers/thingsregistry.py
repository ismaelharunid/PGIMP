

class ThingsRegistry(object):
  
  _cache_name = None
  _cache = None
  
  @property
  def names(self): return self._cache.keys()
  
  @property
  def things(self): return self._cache.viewvalues()
  
  @property
  def asdict(self): return dict(self._cache)
  
  def __init__(self, cache_name='ThingsRegistry'):
    self._cache_name = cache_name
    self._cache = {}
  
  def __str__(self): return ', '.join(self._cache.keys())
  
  def register(self, thing, name=None, overwrite=False):
    if name is None: name = thing.__name__
    if not overwrite and name in self._cache:
      if self._cache[name] != thing:
        raise Exception('name {:s} already exists in {:s}'.format(name, self._cache_name))
      return
    self._cache[name] = thing
  
  def unregister(self, name):
    self._cache.pop(name, None)
  
  def register_many(self, things, overwrite=False):
    for (name, thing) in things.items():
      self.register(thing, name, overwrite)
  


