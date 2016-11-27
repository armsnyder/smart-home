import threading
import time
import random

import phue

import log

# internal state of the fireplace; the data model that drives the simulation
__state = {}

# special internal state value for whether the fireplace process should be running or not
__running = False

# the thread (process) that the fireplace runs on
__thread = None

# time to wait for the fireplace thread to exit in the stop() method
__TIMEOUT = 5.0  # seconds

# get a connection to the Philips Hue Bridge
# the phue library gets a username and ip from a config file located at $USER_HOME/.python_hue
# that is why no ip or username is provided here
__bridge = phue.Bridge()


def start():
    """Start the fireplace process"""
    # any variable that is SET in the method must be declared global
    global __thread, __running
    log.info('Starting the fireplace')
    # if we are already running, do nothing
    if __running:
        log.warn('Fireplace is already running')
        return 409  # HTTP status code: "Conflict"
    # if there is already a fireplace process running, it shouldn't be
    if __thread and __thread.is_alive():
        log.error('Fireplace thread is running')
        return 500  # HTTP status code: "Internal Server Error"
    # set the state to running; the running state is how the main process knows when to stop
    __running = True
    # create a new thread for the main process to run on; the thread is saved so it can be stopped
    __thread = threading.Thread(target=__run)
    # start the fireplace process on the new thread
    __thread.start()
    log.info('Fireplace started')
    return 200  # HTTP status code: "OK"


def stop():
    """Stop the fireplace process"""
    # any variable that is SET in the method must be declared global
    global __running
    if not __running:
        return 400
    log.info('Stopping the fireplace')
    # set running state to false; the main process will halt after its current run loop
    __running = False
    # wait for the main process to finish its final run loop
    __thread.join(__TIMEOUT)
    # if the thread did not stop, there was a problem
    if __thread.is_alive():
        log.error('Fireplace thread did not stop within the specified timeout')
        return 500  # HTTP status code: "Internal Server Error"
    log.info('Fireplace stopped')
    return 200  # HTTP status code: "OK"


def __run():
    """The 'main loop' of the fireplace process"""
    fireplace_id = int(__bridge.get_light_id_by_name('Fireplace'))
    sat = 254
    while __running:
        log.debug('running')
        # for now, just to test, set light 6 to a random color
        # __bridge.set_light(6, 'hue', random.randint(0, 65535))
        bri = random.randint(80, 255)
        hue = random.randint(2000, 11000)
        trans = random.randint(1, 25)
        command = {'bri': bri, 'hue': hue, 'transitiontime': trans, 'sat': sat, 'on': True}
        __bridge.set_light(fireplace_id, command)
        # wait 4 seconds so we don't spam the system
        time.sleep(trans/10)
    __bridge.set_light(fireplace_id, "on", False)
