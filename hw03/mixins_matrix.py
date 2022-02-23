import numbers
import numpy as np


class ConsoleRepresentationMixin:
    def __str__(self):
        return "\n".join(["\t".join(map(str, i)) for i in self._matrix])


class WritingToFileMixin:
    def write_to_file(self, path: str):
        with open(path, 'w') as f:
            f.write(str(self))


class FieldPropertiesMixin:
    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, matrix):
        self._matrix = matrix


class MixinsMatrix(
    np.lib.mixins.NDArrayOperatorsMixin,
    ConsoleRepresentationMixin,
    WritingToFileMixin,
    FieldPropertiesMixin
):

    def __init__(self, matrix):
        self._matrix = np.asarray(matrix)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, self._HANDLED_TYPES + (MixinsMatrix,)):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        inputs = tuple(x._matrix if isinstance(x, MixinsMatrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x._matrix if isinstance(x, MixinsMatrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)