.. :changelog:


History
=======

0.2 (2015-04-24)
----------------

* Use sub-commands for easier extensibility and less ambiguity.
* Move all flag control options to the 'pci-lookup' command.
* Move the PCI device and vendor name look up to their own sub-commands.
* Add LibPCI.lookup_subsystem_device_name().
* Add 'subsystem-device' sub-command.

0.1.1 (2015-04-23)
------------------

* Fix architecture detection bug that prevented libpci from working on Fedora.

0.1 (2015-04-23)
----------------

* First release on PyPI.
