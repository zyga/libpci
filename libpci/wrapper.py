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

"""Pythonic wrapper to some of libpci functions."""

import ctypes
import logging

from libpci._functions import pci_alloc
from libpci._functions import pci_cleanup
from libpci._functions import pci_init
from libpci._functions import pci_lookup_name1
from libpci._functions import pci_lookup_name2
from libpci._functions import pci_lookup_name4
from libpci._types import pci_lookup_mode


__all__ = ('LibPCI',)


_logger = logging.getLogger("libpci")


class flag_property(object):

    """Property exposing a single flag out of a bitmask."""

    def __init__(self, mask, attr_name):
        self.mask = mask
        self.attr_name = attr_name

    def __call__(self, fn):
        self.__doc__ = fn.__doc__
        return self

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = getattr(instance, self.attr_name)
        return bool(value & self.mask)

    def __set__(self, instance, enable):
        value = getattr(instance, self.attr_name)
        if enable:
            value |= self.mask
        else:
            value &= ~self.mask
        setattr(instance, self.attr_name, value)


def _err_closed():
    raise ValueError("attempt to use closed LibPCI object")


class LibPCI(object):

    """
    Pythonic wrapper for libpci.

    This class exposes access to libpci functions in a way that is more
    friendly to work with from Python.

    .. note::
        Not all APIs are supported yet.
    """

    def __init__(self):
        """Initialize the wrapper."""
        _logger.debug("Allocating pci_access")
        self._access = pci_alloc()
        self._flags = 0
        _logger.debug("Got pci_access: %r", self._access)
        _logger.debug("Initializing pci_access")
        pci_init(self._access)

    @property
    def closed(self):
        """Flag determining if libpci resources have been released."""
        return self._access is None

    def close(self):
        """Release libpci resources."""
        if self._access is not None:
            _logger.debug("Cleaning up")
            pci_cleanup(self._access)
        self._access = None

    def __enter__(self):
        """
        Enter a context manager.

        :returns:
            self
        :raises ValueError:
            If :meth:`closed()` is True
        """
        if self.closed:
            _err_closed()
        return self

    def __exit__(self, *args):
        """
        Exit a context manager.

        This method calls :meth:`close()`.
        """
        self.close()

    def __del__(self):
        """Release wrapper resources."""
        self.close()

    @flag_property(pci_lookup_mode.PCI_LOOKUP_NUMERIC, '_flags')
    def flag_numeric(self):
        """Generate numeric names."""

    @flag_property(pci_lookup_mode.PCI_LOOKUP_NO_NUMBERS, '_flags')
    def flag_no_numbers(self):
        """Don't generate numeric names."""

    @flag_property(pci_lookup_mode.PCI_LOOKUP_MIXED, '_flags')
    def flag_mixed(self):
        """Use both names and numbers."""

    @flag_property(pci_lookup_mode.PCI_LOOKUP_NETWORK, '_flags')
    def flag_network(self):
        """Allow network access during lookup."""

    @flag_property(pci_lookup_mode.PCI_LOOKUP_SKIP_LOCAL, '_flags')
    def flag_skip_local(self):
        """Skip local database when performing lookups."""

    @flag_property(pci_lookup_mode.PCI_LOOKUP_CACHE, '_flags')
    def flag_cache(self):
        """Cache names retrieved from the network."""

    @flag_property(pci_lookup_mode.PCI_LOOKUP_REFRESH_CACHE, '_flags')
    def flag_refresh_cache(self):
        """Refresh cache during the next lookup."""

    def lookup_vendor_name(self, vendor_id):
        """
        Lookup the name of a given vendor.

        :param vendor_id:
            PCI vendor identifier
        :ptype vendor_id:
            int
        :returns:
            Name of the PCI vendor.

        .. note::
            Lookup respects various flag properties that impact the behavior
            in case the name cannot be found in the local database. Refer to
            the documentation of each of the ``flag_`` properties.
        """
        buf = ctypes.create_string_buffer(1024)
        _logger.debug("Performing the lookup on vendor %#06x", vendor_id)
        flags = self._flags | pci_lookup_mode.PCI_LOOKUP_VENDOR
        pci_lookup_name1(self._access, buf, ctypes.sizeof(buf), flags,
                         vendor_id)
        return buf.value.decode("utf-8")

    def lookup_device_name(self, vendor_id, device_id):
        """
        Lookup the name of a given device.

        :param vendor_id:
            PCI vendor identifier
        :ptype vendor_id:
            int
        :param device_id:
            PCI device identifier
        :ptype device_id:
            int
        :returns:
            Name of the PCI device.

        .. note::
            Lookup respects various flag properties that impact the behavior
            in case the name cannot be found in the local database. Refer to
            the documentation of each of the ``flag_`` properties.
        """
        buf = ctypes.create_string_buffer(1024)
        _logger.debug("Performing the lookup on vendor:device %#06x:%#06x",
                      vendor_id, device_id)
        flags = self._flags | pci_lookup_mode.PCI_LOOKUP_DEVICE
        pci_lookup_name2(self._access, buf, ctypes.sizeof(buf), flags,
                         vendor_id, device_id)
        return buf.value.decode("utf-8")

    def lookup_subsystem_device_name(
            self, vendor_id, device_id, subvendor_id, subdevice_id):
        """
        Lookup the name of a given subsystem device.

        :param vendor_id:
            PCI vendor identifier
        :ptype vendor_id:
            int
        :param device_id:
            PCI device identifier
        :ptype device_id:
            int
        :param subvendor_id:
            PCI subvendor identifier
        :ptype subvendor_id:
            int
        :param device_id:
            PCI subdevice identifier
        :ptype subdevice_id:
            int
        :returns:
            Name of the PCI subsystem device.

        .. note::
            Lookup respects various flag properties that impact the behavior
            in case the name cannot be found in the local database. Refer to
            the documentation of each of the ``flag_`` properties.
        """
        buf = ctypes.create_string_buffer(1024)
        _logger.debug("Performing the lookup on vendor:device "
                      "subvendor:subdevice %#06x:%#06x %#06x:%#06x",
                      vendor_id, device_id, subvendor_id, subdevice_id)
        flags = self._flags | pci_lookup_mode.PCI_LOOKUP_SUBSYSTEM
        flags = self._flags | pci_lookup_mode.PCI_LOOKUP_DEVICE
        pci_lookup_name4(self._access, buf, ctypes.sizeof(buf), flags,
                         vendor_id, device_id, subvendor_id, subdevice_id)
        return buf.value.decode("utf-8")
