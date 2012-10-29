powerup
=======

powerup is a single serving web application to report power and network
connection status to the web. I wrote it as hurricane Sandy approached on
October 27, 2012 so, if I left the house, I would know whether I would be coming
back to working lights and a cold refrigerator.


Usage
-----

The application is an extremely simple Flask application (see
``requirements.txt`` for a complete list of Python dependencies). You will also
need the following:

* write access to a file named ``status.txt`` in the same directory as
  ``powerup.py``

* file name ``settings.py`` in the same directory as ``powerup.py`` containing
  the application settings (see the `Settings`_ section below)

Please use your preferred WSGI deployment method. Once the application is
running, configure a device to periodically POST to the application with the
device's uptime and the secret token. This works best on an always-on device,
like a router. Here's an example with cURL::

    curl --data-urlencode "token=secrettoken" --data-urlencode "uptime=$(uptime)" http://example.com/update

Then you can quickly and easily check the status at the base URL.


Settings
--------

The ``settings`` module may contain the following settings:

``POWER_TIMEOUT``
    (Default: ``30``) The number of minutes without an update before the
    site reports a power outage.

``SECRET_TOKEN``
    A string containing a secret that only you know about. It's used to discard
    unauthorized update attempts (though you may want to configure your
    webserver to refuse requests to the ``/update`` URL from unexepcted IP
    addresses as well).

Settings with a default value may be omitted.
