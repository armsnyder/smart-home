import phue


running = False
state = {}


def start():
    global running
    running = True
    run()
    return


def stop():
    global running
    running = False
    return


def run():
    global running
    if running:
        flicker()
        run()
    return  # :]


def flicker():
    # b = phue.Bridge('192.168.1.222')
    #
    # b.connect()
    #
    # command = {}
    #
    # b.set_light(6, command)
    return
