import gphoto2 as gp
import os

# global def
event_texts = {
    gp.GP_EVENT_CAPTURE_COMPLETE: "Capture Complete",
    gp.GP_EVENT_FILE_ADDED: "File Added",
    gp.GP_EVENT_FOLDER_ADDED: "Folder Added",
    gp.GP_EVENT_TIMEOUT: "Timeout",
}

camera = gp.Camera()
print('getting camera')
camera.init()
config = camera.get_config()


def change_cfg(name, value):
    """
    Changes the config from the parameter
    """
    item = config.get_child_by_name(name)
    print('Changing config: ' + name + ' to ' + value)
    item.set_value(value)
    print('Succeeded')
    camera.set_config(config)
    return 0


def event_text(event_type):
    if event_type in event_texts:
        return event_texts[event_type]
    return "Unknown Event"


def take_shot(name, nb):
    for i in range(1, nb):
        print("Capture #%1d" % i)

        image = camera.capture(gp.GP_CAPTURE_IMAGE)

        file = camera.file_get(image.folder, image.name, gp.GP_FILE_TYPE_NORMAL)
        destination = os.path.join(os.getcwd(), name + image.name)

        file.save(destination)
        print("saved to " + destination)

        # empty the event queue
        typ, data = camera.wait_for_event(200)
        while typ != gp.GP_EVENT_TIMEOUT:

            print("Event: %s, data: %s" % (event_text(typ), data))

            if typ == gp.GP_EVENT_FILE_ADDED:
                file = os.path.join(data.folder, data.name)
                print("New file: %s" % file)
            # self.download_file(fn)

            # try to grab another event
            typ, data = camera.wait_for_event(1)


def change_man_cfg(iso, aperture, shutter_speed):
    """
    wrapper function to help with managing manual photo config
    """
    print("changing config to: iso: " + iso + ", aperture: " + aperture + ", shutterspeed: " + shutter_speed)
    change_cfg('iso', iso)
    change_cfg('aperture', aperture)
    change_cfg('shutterspeed', shutter_speed)
    return 0


def take_darks():
    """
    Take dark for calibrating the iso
    """
    print("Taking dark frames")
    change_man_cfg('6400', '3.5', '1/8000')
    take_shot('darks/', 20)


def take_biases():
    """
    Calibrate the noise by taking bias frames
    """
    print("Taking bias frames")
    change_man_cfg('6400', '3.5', '1')
    take_shot('biases/', 20)


def take_flats():
    """
    Calibrate the color by taking shots of even light
    """
    print("Taking flats frames")
    input(
        "Put paper in front of your camera and put your phone in the white background, or do it in the sun\npress "
        "enter once done")
    change_man_cfg('6400', '3.5', '1/80')
    take_shot('flats/', 20)


def take_lights():
    """
    Taking pictures
    """
    print("Taking light frames")
    change_man_cfg('6400', '3.5', '1')
    take_shot('lights/', 2)

print('SUCCESS!!!')
