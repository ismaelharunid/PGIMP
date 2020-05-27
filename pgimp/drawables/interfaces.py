

import PIL
from PIL import ImageFont
from PIL.ImageDraw import *
from collections import Sequence, Mapping
from numbers import Number
from ..helpers.method_hijacker import Interface, NOT_RECOMMENDED \
    , create_abstract_class, create_proxy_class
from ..helpers.thingsregistry import ThingsRegistry


CONSTANTS = ThingsRegistry('CONSTANTS')
INTERFACES = ThingsRegistry('INTERFACES')
MIXINS = ThingsRegistry('MIXINS')


# A class combining functionality of Image and ImageDraw classes.
# The basic startegy is to extend the ImageDraw class and add Image class
# methods to eliminate having to maintain both Image and ImageDraw instances.
# Note that the constructor uses reversed order to allow for a default image
# mode.


issequence = lambda obj, size=None, type=Sequence, itemtype=None: \
     isinstance(obj, Sequence) \
     and (size is None or size == len(obj)) \
     and (itemtype is None or all(isinstance(c, itemtype) for c in obj))
istuplish = lambda obj, size=None, itemtype=None: \
    issequence(obj, size, tuple, itemtype)


def rect_intersect(rect0, *rects):
  rect = list(rect0)
  for r in rects:
    if rect[0] > r[0]: rect[0] = r[0]
    if rect[1] > r[1]: rect[1] = r[1]
    if rect[2] < r[2]: rect[2] = r[2]
    if rect[3] < r[3]: rect[3] = r[3]
  return type(rect0)(rect)


def xy_flatten(xy, n_coords=None, offset=(0,)):
  if not xy:
    return ()
  if isinstance(xy, Sequence):
    if isinstance(xy[0], Sequence):
      if n_coords is None: n_coords = len(xy[0])
      if all(n_coords != len(c) for c in xy):
        raise IndexError('bad shape ({:d},{:d} to {:d}), expected second axis length of {:d}' \
            .format(len(xy), min(len(c) for c in xy), max(len(c) for c in xy) \
            , n_coords))
    else:
      if n_coords is None:
        n_coords = 2
      if len(xy) % n_coords:
        raise IndexError('bad shape ({:d}), expected a length on {:d} boundaries ' \
            .format(len(xy), n_coords))
  elif hasattr(xy, 'totuple'):
    return xy_flatten(xy.totuple())
  elif hasattr(xy, 'tolist'):
    return xy_flatten(xy.tolist())
  else:
    raise TypeError('bad xy type {:s}, expected a '.format(type(xy).__name__) \
        + 'Sequence, np.ndarray or object with a "tolist" or "totuple? method')
  
  if offset is not None:
    if isinstance(offset, Number):
      offsets = (offset,)
    if len(offset) != n_coords:
      offset = (tuple(offset) * n_coords)[:n_coords]
    coord_indexes = tuple(range(n_coords))
    if isinstance(xy[0], Sequence):
      return sum((tuple(c[i]+offset[i] for i in coord_indexes) for c in xy), ())
    else:
      return sum((tuple(xy[j+i:j+i+n_coords]+offset[i] for i in coord_indexes) \
          for j in range(0,len(xy),n_coords)), ())
  
  if isinstance(xy[0], Sequence):
    return sum((tuple(c) for c in xy), ())
  
  return xy if type(xy) is tuple else tuple(xy)


def npa_smoothing(npa, closed=False, smoothing=10, method='cubic', n_coords=None):
  """TODO: make this into an iterator.  It only needs 2 points on either side
     so it's very doable"""
  if n_coords is None:
    if isinstance(npa, np.ndarray):
      n_coords = npa.shape[1]
    elif isinstance(npa, Sequence) and isinstance(npa[0], Sequence):
      n_coords = len(npa[0])
    else:
      raise Exception('invalid sequence or array')
  assert n_coords > 1 \
      , 'the n_coords argument must be set when using flat sequences or array'
  npa = np.reshape(npa, (-1, n_coords)).astype(np.float64)
  n_points = len(npa)
  if closed:    # encapsilate wraparpund
    npa = np.vstack( (npa[-3:-1], npa, npa[1:3]) )
    start, stop = 2, n_points + 2
    n_req_points = int(sum(npa_dists(npa,start,stop+1)) / smoothing)
  else:
    start, stop = 0, n_points
    n_req_points = int(sum(npa_dists(npa,start,stop)) / smoothing)
  t = np.arange(n_points)
  ti = np.linspace(start, stop-1, n_req_points)
  return np.array(tuple( interp1d(t, npa[:,i], kind=method)(ti) \
      for i in range(n_coords)), dtype=np.float64).swapaxes(0,1)


class Drawable(Interface):
  
  _basetype = None
  _xtype    = None
  _bpp      = None
  _size     = None
  _offset   = None
  _parent   = None
  
  # 
  # private methods
  # 
  
  def _retype(self, basetype=None, xtype=None, bpp=None):
    raise NotImplementedError('call to non-implemented method {:s}#{:s}(...)'
        .format(self.__class__.__name__, self.__name__))
  
  def _resize(self, size=None, offset=None):
    raise NotImplementedError('call to non-implemented method {:s}#{:s}(...)'
        .format(self.__class__.__name__, self.__name__))
  
  def _get_bounds(self):
    frame = self.offset + self._offset
  
  def _get_frame(self, clip=False):
    frame = list(self._get_bounds())
    if isinstance(self._parent, Drawable):
      parent_frame = _parent._get_frame()
      frame[0], frame[1] = parent_frame[0] + frame[0], parent_frame[1] + frame[1]
      if clip:
        frame = rect_intersect(frame, parent_frame)
    return frame
  
  # 
  # read-only public properties
  # 
  
  @property
  def bounds(self): return self._get_bounds()
  
  @property
  def frame(self): return self._get_frame()

  @property
  def x0(self): return self._get_frame()[0]

  @property
  def y0(self): return self._get_frame[1]

  @property
  def x1(self): return self._get_frame[2]

  @property
  def y1(self): return self._get_frame[3]
  
  # 
  # writable public properties
  # 
  
  @property
  def basetype(self): return self._basetype
  
  @basetype.setter
  def basetype(self, basetype):
    self._retype(basetype=basetype)
  
  @property
  def xtype(self): return self._xtype
  
  @xtype.setter
  def xtype(self, xtype):
    self._retype(xtype=xtype)
  
  @property
  def bpp(self): return self._bpp
  
  @bpp.setter
  def bpp(self, bpp):
    if not isinstance(bpp, Number):
      raise TypeError('setter {:s}#{:s} excepts an number, but received {:s}'
          .format(self.__class__.__name__, self.__name__, type(bpp).__name__))
    self._retype(bpp=bpp)
  
  @property
  def size(self): return self._size
  
  @size.setter
  def size(self, size):
    if not issequence(size, 2, itemtype=Number):
      raise TypeError('setter {:s}#{:s} excepts a 2-tuplish containing numbers, but received {:s}'
          .format(self.__class__.__name__, self.__name__, repr(size)))
    self._resize(size)

  @property
  def width(self): return self._size[0]

  @width.setter
  def width(self, width):
    if not isinstance(width, Number):
      raise TypeError('setter {:s}#{:s} excepts an int, but received {:s}'
          .format(self.__class__.__name__, self.__name__, type(width).__name__))
    self._resize((width, self._size[1]))

  @property
  def height(self): return self._size[1]
  
  @height.setter
  def height(self, height):
    if not isinstance(height, Number):
      raise TypeError('setter {:s}#{:s} excepts an int, but received {:s}'
          .format(self.__class__.__name__, self.__name__, type(height).__name__))
    self._resize((self._size[0], height))

  @property
  def offset(self): return self._offset

  @offset.setter
  def offset(self, offset):
    if not issequence(offset, 2, itemtype=Number):
      raise TypeError('setter {:s}#{:s} excepts a 2-tuplish, but received {:s}'
          .format(self.__class__.__name__, self.__name__, type(size).__name__))
    self._resize(offset=offset)

  @property
  def offset_x(self): return self._offset[0]

  @offset_x.setter
  def offset_x(self, offset_x):
    if not isinstance(offset_x, Number):
      raise TypeError('setter {:s}#{:s} excepts an int, but received {:s}'
          .format(self.__class__.__name__, self.__name__, type(offset_x).__name__))
    self._resize(offset=(offset_x, self._offset[1]))

  @property
  def offset_y(self): return self._offset[1]

  @offset_y.setter
  def offset_y(self, offset_y):
    if not isinstance(offset_y, Number):
      raise TypeError('setter {:s}#{:s} excepts an int, but received {:s}'
          .format(self.__class__.__name__, self.__name__, type(offset_y).__name__))
    self._resize(offset=(self._offset[0], offset_y))
  
  # 
  # public instance methods
  #
  
  def resize(self, size, offset=None):
    self._resize(size, offset)

INTERFACES.register(Drawable)


class Channel(Drawable):
  """ a single channel Drawable"""

INTERFACES.register(Channel)


class Renderable(Drawable):
  """ a dynamic renderable Drawable"""

INTERFACES.register(Renderable)


class Text(Renderable):
  """ a single channel Drawable"""

INTERFACES.register(Text)


class Vector(Renderable):
  """ a single channel Drawable"""

INTERFACES.register(Vector)


class Faces(Vector):
  """ a single channel Drawable"""

INTERFACES.register(Faces)


class Model(Faces):
  """ a single channel Drawable"""

INTERFACES.register(Model)




DRAWABLE_METHOD_NAMES = """alpha_composite, close, convert, copy, crop, draft, effect_spread, filter, format, format_description, frombytes, fromstring, getbands, getbbox, getchannel, getcolors, getdata, getextrema, getim, getpalette, getpixel, getprojection, histogram, line, load, paste, polygon, putalpha, putdata, putpalette, putpixel, quantize, remap_palette, resize, rotate, save, seek, show, split, tell, thumbnail, tobitmap, tobytes, toqimage, toqpixmap, tostring, transform, transpose, verify"""


