
from ..helpers.thingsregistry import ThingsRegistry
from interfaces import CONSTANTS, INTERFACES, MIXINS

import constants, simple, tiled, layered, renderable, text, vector, model
globals().update(CONSTANTS.asdict)
globals().update(INTERFACES.asdict)
globals().update(MIXINS.asdict)
CLASSES = ThingsRegistry('CLASSES')

isinterface = lambda thing: thing in INTERFACES.things
ismixin = lambda thing: thing in MIXINS.things
isclass = lambda thing: thing in CLASSES.things


class SimpleDrawable(Drawable, SimpleMixin):
  pass

CLASSES.register(SimpleDrawable)


class SimpleChannel(Channel, SimpleMixin):
  pass

CLASSES.register(SimpleChannel)


class TiledDrawable(Drawable, TiledMixin):
  pass

CLASSES.register(TiledDrawable)


class TiledChannel(Channel, TiledMixin):
  pass

CLASSES.register(TiledChannel)


class LayeredDrawable(Drawable, LayeredMixin):
  pass

CLASSES.register(LayeredDrawable)


class LayeredChannel(Channel, LayeredMixin):
  pass

CLASSES.register(LayeredChannel)


class LayeredTiledDrawable(Drawable, TiledMixin, LayeredMixin):
  pass

CLASSES.register(LayeredTiledDrawable)


class LayeredTiledChannel(Channel, TiledMixin, LayeredMixin):
  pass

CLASSES.register(LayeredTiledChannel)



