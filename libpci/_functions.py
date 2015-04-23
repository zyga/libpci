# encoding: utf-8
#
# Copyright 2015 Canonical Ltd.
#
# Written by:
#   Zygmunt Krynicki <zygmunt.krynicki@canonical.com>
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

"""Low-level interface to libpci (using ctypes)."""

import ctypes

from libpci._native import Function
from libpci._native import IN
from libpci._types import pci_access


# Shared library object


libpci = ctypes.cdll.LoadLibrary("libpci.so.3")


# Functions

@Function(libpci)
def pci_alloc() -> ctypes.POINTER(pci_access):
    """
    Allocate a pci_access object.

    struct pci_access *pci_alloc(void) PCI_ABI;.
    """
    pass


@Function(libpci)
def pci_init(access: (IN, ctypes.POINTER(pci_access))) -> None:
    """
    Initialize a pci_access object.

    void pci_init(struct pci_access *) PCI_ABI;
    """
    pass


@Function(libpci)
def pci_cleanup(access: (IN, ctypes.POINTER(pci_access))) -> None:
    """
    Clean up a pci_access object.

    void pci_cleanup(struct pci_access *) PCI_ABI;
    """
    pass


# Calling convention for pci_lookup_name()
# ========================================
#
# Call pci_lookup_name() to identify different types of ID's:
#
#   VENDOR              (vendorID) -> vendor
#   DEVICE              (vendorID, deviceID) -> device
#   VENDOR | DEVICE         (vendorID, deviceID) -> combined vendor and device
#   SUBSYSTEM | VENDOR      (subvendorID) -> subsystem vendor
#   SUBSYSTEM | DEVICE      (vendorID, deviceID, subvendorID, subdevID)
#                               -> subsystem device
#   SUBSYSTEM | VENDOR | DEVICE (vendorID, deviceID, subvendorID, subdevID)
#                               -> combined subsystem v+d
#   SUBSYSTEM | ...         (-1, -1, subvendorID, subdevID)
#                               -> generic subsystem
#   CLASS               (classID) -> class
#   PROGIF              (classID, progif) -> programming interface


@Function(libpci, "pci_lookup_name")
def pci_lookup_name1(
    access: (IN, ctypes.POINTER(pci_access)),
    buf: (IN, ctypes.c_char_p),
    size: (IN, ctypes.c_int),
    flags: (IN, ctypes.c_int),
    arg1: (IN, ctypes.c_int),
) -> ctypes.c_char_p:
    """
    Conversion of PCI ID's to names (according to the pci.ids file).

    char *pci_lookup_name(
        struct pci_access *a, char *buf, int size, int flags, ...
    ) PCI_ABI;

    This is a variant of pci_lookup_name() that gets called with one argument.
    It is required because ctypes doesn't support varadic functions.
    """
    pass


@Function(libpci, "pci_lookup_name")
def pci_lookup_name2(
    access: (IN, ctypes.POINTER(pci_access)),
    buf: (IN, ctypes.c_char_p),
    size: (IN, ctypes.c_int),
    flags: (IN, ctypes.c_int),
    arg1: (IN, ctypes.c_int),
    arg2: (IN, ctypes.c_int),
) -> ctypes.c_char_p:
    """
    Conversion of PCI ID's to names (according to the pci.ids file).

    char *pci_lookup_name(
        struct pci_access *a, char *buf, int size, int flags, ...
    ) PCI_ABI;

    This is a variant of pci_lookup_name() that gets called with two arguments.
    It is required because ctypes doesn't support varadic functions.
    """
    pass


@Function(libpci, "pci_lookup_name")
def pci_lookup_name4(
    access: (IN, ctypes.POINTER(pci_access)),
    buf: (IN, ctypes.c_char_p),
    size: (IN, ctypes.c_int),
    flags: (IN, ctypes.c_int),
    arg1: (IN, ctypes.c_int),
    arg2: (IN, ctypes.c_int),
    arg3: (IN, ctypes.c_int),
    arg4: (IN, ctypes.c_int),
) -> ctypes.c_char_p:
    """
    Conversion of PCI ID's to names (according to the pci.ids file).

    char *pci_lookup_name(
        struct pci_access *a, char *buf, int size, int flags, ...
    ) PCI_ABI;

    This is a variant of pci_lookup_name() that gets called with four
    arguments. It is required because ctypes doesn't support varadic functions.
    """
    pass


# Automatically-generated __all__
__all__ = tuple(name for name in locals().keys() if name.startswith('pci_'))
