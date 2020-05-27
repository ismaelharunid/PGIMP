

from interfaces import *

class SimpleMixin(object):
  _image  = None
  _offset = (0,0)
  
  def __init__(self, size, mode="RGBA", background_color=0, offset=(0,0)):
    """
    constructs a SimpleDrawable instance.

    :param size: A 2 tuple as the size of the drawable (or PIL.Image.Image instance)
    :param mode: The drawable mode, defaults to "RGBA".
    :param background_color: The fill color for the drawable.
    :param offset: A 2 tuple as the offset of the drawable.
    :returns:  An :py:class:SimpleDrawable` object.

    """
    image = size if isinstance(size, PIL.Image.Image) else \
        PIL.Image.new(mode, size, background_color)
    super(self.__class__, self).__init__(image, mode)
    self._image = image
    self._offset = offset
  
  @property
  def width(self): return self._image.size[0]

  @property
  def height(self): return self._image.size[1]

  @property
  def size(self): return self._image.size

  @property
  def offset_x(self): return self._offset[0]

  @property
  def offset_y(self): return self._offset[1]

  @property
  def offset(self): return self._offset

  def polygon(self, xy
      , fill_color=None
      , outline_color=None, outline_width=1   #, joint=None
      , closed=True, smoothing=None):
    """Draw a polygon."""
    if smoothing is not None:
      xy = npa_smoothing(xy, closed, smoothing, 'cubic')
    fpd = xy_flatten(xy, 2, self.offset)
    super(self.__class__, self).polygon(fpd, fill_color)
    if outline_color or outline_width:
      super(self.__class__, self).line(fpd+fpd[:2] if closed else fpd
          , outline_color, outline_width)   #, joint)
  
  def line(self, xy
      , outline_color=None, outline_width=1, joint=None, smoothing=None):
    """Draw a line, or a connected sequence of line segments."""

    if smoothing is not None:
      xy = npa_smoothing(xy, False, smoothing, 'cubic')
    super(self.__class__, self).line(xy_flatten(xy, 2, self.offset)
        , outline_color, outline_width)   #, joint)


# create_proxy_class(NOT_RECOMMENDED, SimpleMixin, '_image'
    # , PIL.Image.Image, """alpha_composite, close, convert, copy, crop, draft, effect_spread, filter, format, format_description, frombytes, fromstring, getbands, getbbox, getchannel, getcolors, getdata, getextrema, getim, getpalette, getpixel, getprojection, histogram, line, load, paste, polygon, putalpha, putdata, putpalette, putpixel, quantize, remap_palette, resize, rotate, save, seek, show, split, tell, thumbnail, tobitmap, tobytes, toqimage, toqpixmap, tostring, transform, transpose, verify""")

MIXINS.register(SimpleMixin)
