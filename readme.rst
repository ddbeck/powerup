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

* a file name ``settings.py`` in the same directory as ``powerup.py`` containing
  a string assigned to ``SECRET_TOKEN`` that only you know about

Please use your preferred WSGI deployment method. Once the application is
running, configure a device to periodically POST to the application with the
device's uptime and the secret token. This works best on an always-on device,
like a router. Here's an example with cURL::

    curl --data-urlencode "token=secrettoken" --data-urlencode "uptime=$(uptime)" example.com/update

Then you can quickly and easily check the status at the base URL.
