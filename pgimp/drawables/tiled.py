

from interfaces import *


class TiledMixin(object):
  
  _size     = None
  _tilesize = None
  _tiles    = None
  _offset   = (0,0)
  
  def __init__(self, size, tilesize, mode="RGBA", background_color=0, offset=(0,0)):
    pass  # placeholder


MIXINS.register(TiledMixin)
