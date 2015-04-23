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

"""Type definitions and enumerations found in pci.h."""

import ctypes
import enum
import os

# Hand-crafted enum definitions


class pci_access_type(enum.IntEnum):

    """enum pci_access_type from pci.h."""

    PCI_ACCESS_AUTO = 0
    PCI_ACCESS_SYS_BUS_PCI = 1
    PCI_ACCESS_PROC_BUS_PCI = 2
    PCI_ACCESS_I386_TYPE1 = 3
    PCI_ACCESS_I386_TYPE2 = 4
    PCI_ACCESS_FBSD_DEVICE = 5
    PCI_ACCESS_AIX_DEVICE = 6
    PCI_ACCESS_NBSD_LIBPCI = 7
    PCI_ACCESS_OBSD_DEVICE = 8
    PCI_ACCESS_DUMP = 9
    PCI_ACCESS_MAX = 10


class pci_lookup_mode(enum.IntEnum):

    """enum pci_lookup_mode from pci.h."""

    PCI_LOOKUP_VENDOR = 1
    PCI_LOOKUP_DEVICE = 2
    PCI_LOOKUP_CLASS = 4
    PCI_LOOKUP_SUBSYSTEM = 8
    PCI_LOOKUP_PROGIF = 16
    PCI_LOOKUP_NUMERIC = 0x10000
    PCI_LOOKUP_NO_NUMBERS = 0x20000
    PCI_LOOKUP_MIXED = 0x40000
    PCI_LOOKUP_NETWORK = 0x80000
    PCI_LOOKUP_SKIP_LOCAL = 0x100000
    PCI_LOOKUP_CACHE = 0x200000
    PCI_LOOKUP_REFRESH_CACHE = 0x400000


# Hand crafted type declarations


class id_entry(ctypes.Structure):

    """struct id_entry (private)."""


class id_bucket(ctypes.Structure):

    """struct id_bucket (private)."""


class pci_methods(ctypes.Structure):

    """struct pci_methods (private)."""


class pci_filter(ctypes.Structure):

    """struct pci_filter from pci.h."""

    _fields_ = [
        ('domain', ctypes.c_int),
        ('bus', ctypes.c_int),
        ('slot', ctypes.c_int),
        ('func', ctypes.c_int),
        ('vendor', ctypes.c_int),
        ('device', ctypes.c_int),
    ]


class pci_cap(ctypes.Structure):

    """struct pci_cap from pci.h."""


pci_cap._fields_ = [
    ('next', ctypes.POINTER(pci_cap)),
    ('id', ctypes.c_uint16),
    ('type', ctypes.c_uint16),
    ('addr', ctypes.c_uint),
]


class pci_param(ctypes.Structure):

    """struct pci_param from pci.h."""


pci_param._fields_ = [
    ('pci_param', ctypes.POINTER(pci_param)),
    ('param', ctypes.c_char_p),
    ('value', ctypes.c_char_p),
    ('value_malloced', ctypes.c_int),
    ('help', ctypes.c_char_p),
]


# XXX: this can be uint32 as well, depending on configuration
if os.uname().machine in ('x86_64', 'aarch64', 'ppcel64'):
    pciaddr_t = ctypes.c_uint64
else:
    pciaddr_t = ctypes.c_uint32


class pci_dev(ctypes.Structure):

    """struct pci_dev from pci.h."""


class pci_access(ctypes.Structure):

    """struct pci_access from pci.h."""

pci_dev._fields_ = [
    ('next', ctypes.POINTER(pci_dev)),
    ('domain', ctypes.c_uint16),
    ('bus', ctypes.c_uint8),
    ('dev', ctypes.c_uint8),
    ('func', ctypes.c_uint8),
    ('known_fields', ctypes.c_int),
    ('vendor_id', ctypes.c_uint16),
    ('device_id', ctypes.c_uint16),
    ('device_class', ctypes.c_uint16),
    ('irq', ctypes.c_int),
    ('base_addr', pciaddr_t * 6),
    ('size', pciaddr_t * 6),
    ('rom_base_addr', pciaddr_t),
    ('rom_file', pciaddr_t),
    ('first_cap', ctypes.POINTER(pci_cap)),
    ('phy_slot', ctypes.c_char_p),
    ('module_alias', ctypes.c_char_p),
    ('access', ctypes.POINTER(pci_access)),
    ('methods', ctypes.POINTER(pci_methods)),
    ('cache', ctypes.POINTER(ctypes.c_uint8)),
    ('cache_len', ctypes.c_int),
    ('hdrtype', ctypes.c_int),
    ('aux', ctypes.c_void_p),
]


pci_access._fields_ = [
    ('method', ctypes.c_uint),
    ('writable', ctypes.c_int),
    ('buscentric', ctypes.c_int),
    ('id_file_name', ctypes.c_char_p),
    ('free_id_name', ctypes.c_int),
    ('numeric_ids', ctypes.c_int),
    ('id_lookup_mode', ctypes.c_uint),
    ('debugging', ctypes.c_int),
    ('error', ctypes.CFUNCTYPE(None, ctypes.c_char_p)),
    ('warning', ctypes.CFUNCTYPE(None, ctypes.c_char_p)),
    ('debug', ctypes.CFUNCTYPE(None, ctypes.c_char_p)),
    ('devices', ctypes.POINTER(pci_dev)),
    ('methods', ctypes.POINTER(pci_methods)),
    ('params', ctypes.POINTER(pci_param)),
    ('id_hash', ctypes.POINTER(ctypes.POINTER(id_entry))),
    ('current_id_bucket', ctypes.POINTER(id_bucket)),
    ('id_load_failed', ctypes.c_int),
    ('id_cache_status', ctypes.c_int),
    ('fd', ctypes.c_int),
    ('fd_rw', ctypes.c_int),
    ('fd_pos', ctypes.c_int),
    ('fd_vpd', ctypes.c_int),
    ('cached_dev', ctypes.POINTER(pci_dev))
]
