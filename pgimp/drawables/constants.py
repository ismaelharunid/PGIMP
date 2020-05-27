
from ..helpers.common import define_constants, enumerate_constants, maskerate_constants
from interfaces import CONSTANTS


#CONSTANTS.register(0, 'NORMAL_MODE')

#define_constants(tokens, max_length=8, prefix='', suffix='')
#enumerate_constants(tokens, max_length=8, prefix='', suffix='')
#maskerate_constants(tokens, max_length=8, prefix='', suffix='')

CONSTANTS.register_many(define_constants('normal', prefix='MODE_'))
