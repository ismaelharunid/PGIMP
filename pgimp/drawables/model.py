
from vector import *


class FaceMixin(VectorMixin):
  pass

MIXINS.register(FaceMixin)


class ModelMixin(FaceMixin):
  pass

MIXINS.register(ModelMixin)
