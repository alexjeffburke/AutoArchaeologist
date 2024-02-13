import sys

from .Wang.wang_text import WangText

__all__ = [
    "WangText"
]

INTERPRETATIONS = {name:getattr(sys.modules[__name__], name) for name in __all__}

def grab_examiner(examiner_name):
    if examiner_name not in INTERPRETATIONS:
        raise LookupError(f'no interpretation named "{examiner_name}"')
    return INTERPRETATIONS[examiner_name]
