# encoding: UTF-8
#
# Copyright (c) 2015 Canonical Ltd.
#
# Author: Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
native -- high-level wrapper for ctypes.

This module contains the :func:`native()` function which aids in creating
type-safe, discoverable and documented bindings to functions in dynamically
linked libraries.

This module requires Python 3.4
"""
from collections import namedtuple
from ctypes import CDLL
from ctypes import CFUNCTYPE
from enum import IntEnum
from inspect import Parameter
from inspect import Signature
from inspect import signature

__all__ = ('Function', 'IN', 'OUT', 'Macro')


# NOTE: a bitmask flag would have been better
class ArgFlag(IntEnum):
    IN = 1
    OUT = 2
    ZERO = 4


IN = ArgFlag.IN
OUT = ArgFlag.OUT
ZERO = ArgFlag.ZERO


metadata = namedtuple("metadata", "restype argtypes paramflags")


def _ctypes_metadata(fn):
    sig = signature(fn)
    if sig.return_annotation is Signature.empty:
        raise TypeError("missing return type annotation")
    restype = sig.return_annotation
    argtypes = []
    paramflags = []
    for param in sig.parameters.values():
        if param.annotation is Parameter.empty:
            raise TypeError(
                "missing annotation on parameter {}".format(param.name))
        if (not isinstance(param.annotation, tuple)
                or not len(param.annotation) in (2, 3)):
            raise TypeError(
                "incorrect annotation on parameter {}".format(param.name))
        if param.kind != Parameter.POSITIONAL_OR_KEYWORD:
            raise TypeError(
                "incorrect kind of parameter {}".format(param.name))
        if len(param.annotation) == 2:
            param_flags, param_type = param.annotation
            param_default = param.default
        else:
            param_flags, param_type, param_default = param.annotation
        if param_default is not Parameter.empty:
            if param_flags == IN and param_default == 0:
                paramflags.append(
                    (int(param_flags | ZERO), param.name))
            else:
                paramflags.append(
                    (int(param_flags), param.name, param_default))
        else:
            paramflags.append((int(param_flags), param.name))
        argtypes.append(param_type)
    return metadata(restype, tuple(argtypes), tuple(paramflags))


def Function(
    library: CDLL,
    name_or_ordinal: 'Union[str, int, None]'=None,
    proto_factory: ('Union[ctypes.CFUNCTYPE, ctypes.WINFUNCTYPE,'
                    ' ctypes.PYFUNCTYPE]')=CFUNCTYPE,
    use_errno: bool=False,
    use_last_error: bool=False,
) -> 'Callable':
    """
    Decorator factory for creating callables for native functions.

    Decorator factory for constructing relatively-nicely-looking callables that
    call into existing native functions exposed from a dynamically-linkable
    library.

    :param library:
        The library to look at
    :param name_or_ordinal:
        Typically the name of the symbol to load from the library.  In rare
        cases it may also be the index of the function inside the library.
    :param proto_factory:
        The prototype factory.
    :param use_last_error:
        Passed directly to the prototype factory.
    :param use_last_error:
        Passed directly to the prototype factory.
    :returns:
        A decorator for a function with particular, special annotations.

    .. note::
        Since nested functions have hard-to-reach documentation, the
        documentation of the function returned from ``native()`` is documented
        below.
    """
    def decorator(fn: 'Callable') -> 'Callable':
        metadata = _ctypes_metadata(fn)
        prototype = proto_factory(
            metadata.restype, *metadata.argtypes,
            use_errno=use_errno, use_last_error=use_last_error)
        func_spec = (name_or_ordinal or fn.__name__, library)
        return prototype(func_spec, metadata.paramflags)
    return decorator


class Macro(object):

    """A preprocessor macro-like thing."""

    def __init__(self, name, value):
        """Initialize a macro with a name and value."""
        self.name = name
        self.value = value

    def __repr__(self):
        """Get a debugging representation of the macro."""
        return '<{}: {!r}>'.format(self.name, self.value)

    def __str__(self):
        """Get string version of the value of the macro."""
        return str(self.value)

    @property
    def _as_parameter_(self):
        return self.value
