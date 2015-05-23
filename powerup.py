"""A single serving site to report on power and internet connection."""

from flask import Flask, request, render_template
import os
import datetime

app = Flask(__name__, template_folder='templates')
app.config['STATUS_FILE'] = 'status.txt'
app.config['POWER_TIMEOUT'] = 30
app.config['ACTIVE'] = True
app.config.from_object('settings')


class NoTimeFileError(Exception):
    pass


def get_power_info():
    """Returns a dictionary with the following key-value pairs:

    ``up``: whether the status file has been updated in the past thirty minutes
    ``last_update``: minutes since the last update
    ``uptime``: the last update's uptime key-value
    """
    try:
        mtime = os.path.getmtime(app.config['STATUS_FILE'])
        with open(app.config['STATUS_FILE']) as fp:
            uptime = fp.read()
    except OSError:
        raise NoTimeFileError

    delta = (datetime.datetime.now() -
             datetime.datetime.fromtimestamp(mtime))

    return {
        'up': (delta.seconds // 60) < app.config['POWER_TIMEOUT'],
        'last_updated': delta.seconds // 60,
        'uptime': uptime,
    }


@app.route("/")
def status():
    """Get the current status."""
    ctx = {'error': None}

    if not app.config['ACTIVE']:
        ctx['error'] = "This site is disabled, so who cares if the power's on?"

    try:
        ctx.update(get_power_info())
    except NoTimeFileError:
        ctx['error'] = (
            'Who knows if the power is on? The status file is missing!')

    return render_template('powerup.html', **ctx)


@app.route("/update", methods=['POST'])
def update():
    """Store the current status in a file. Requires a secret token specified by
    the application's ``SECRET_TOKEN`` setting.
    """
    headers = {'Content-Type': 'text/plain'}

    token = request.form.get('token', None)
    uptime = request.form.get('uptime', None)

    if token == app.config['SECRET_TOKEN'] and uptime is not None:
        with open(app.config['STATUS_FILE'], 'w') as fp:
            fp.write(uptime)
        return (
            "Accepted update at: {}".format(datetime.datetime.now()),
            200,
            headers
        )
    else:
        return (
            u'Unacceptable! One million years dungeon!',
            403,
            headers
        )


if __name__ == "__main__":
    app.run(debug=True)
