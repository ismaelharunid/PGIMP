

from interfaces import *


class LayeredMixin(object):
  
  _children = None
  _rendered = False
  
  def __init__(self, size, mode="RGBA", background_color=0, offset=(0,0)):
    """
    constructs a SimpleDrawable instance.

    :param size: A 2 tuple as the size of the drawable
    :param mode: The drawable mode, defaults to "RGBA".
    :param background_color: The fill color for the drawable.
    :param offset: A 2 tuple as the offset of the drawable.
    :returns:  An :py:class:SimpleDrawable` object.

    """
    self._children = []
    if isinstance(size, PIL.Image.Image):
      child, size = size, size.size   # first layer
      self.adopt_child(child)
    super(self.__class__, self).__init__(size, mode="RGBA", background_color=0, offset=(0,0))
  
  @property
  def n_children(self): return len(self._children)
  
  @property
  def children(self): return tuple(self._children)
  
  def adopt_child(self, child_drawable, position=None):
    if not isinstance(child, PIL.Image.Image):
      raise Exception()
    if not isinstance(child, Drawable):
      child = SimpleDrawable(child)
    if position is None: position = len(self._children)
    self._children.insert(position, child)
    self._rendered = False
    return child
  
  def orphan_child(self, child_drawable, position=None):
    self._children.remove(child)
    self._rendered = False
    return child
  
  def swap_children(self, children, where=None):
    #  where = lambda self, child0, child1, index0, index1: True
    child = children[0]
    if isinstance(child, Sequence):
      child = self.swap_children(child)
    if type(child) is int:
      index, child = child, self._children.index(children[index])
    else:
      index = self._children.index(child)
    for child in children[1:]:
      prev_child, prev_index = child, index
      if isinstance(child, Sequence):
        child = self.swap_children(child)
      if type(child) is int:
        index, child = child, self._children.index(children[index])
      else:
        index = self._children.index(child)
      # some pythons variants don't correctly observe assignment operation order
      if where is None or where(self, child0, child1, index0, index1):
        swap = self._children[prev_index], self._children[index]  
        self._children[index], self._children[prev_index] = swap
    return self._children[index]


MIXINS.register(LayeredMixin)

