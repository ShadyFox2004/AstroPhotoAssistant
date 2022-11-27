import time
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
    '''
    Changes the config from the parameter
    '''
    item = config.get_child_by_name(name)
    print('Changing config: ' + name + ' to ' + value)
    item.set_value(value)
    print('Succeded')
    camera.set_config(config)
    return(0);

def event_text(event_type):
	if event_type in event_texts:
		return event_texts[event_type]
	return "Unknown Event"

def takeShot(name, nb):
	for i in range(1,nb):
		print("Capture #%1d" % i)

		image = camera.capture(gp.GP_CAPTURE_IMAGE)

		file = camera.file_get(image.folder,image.name,gp.GP_FILE_TYPE_NORMAL)
		dest = os.path.join(name+image.name)

		file.save(dest)
		print("saved to '%s'" % dest2)
	
		#empty the event queue
		typ,data = camera.wait_for_event(200)
		while typ != gp.GP_EVENT_TIMEOUT:
		
			print("Event: %s, data: %s" % (event_text(typ),data))
		
			if typ == gp.GP_EVENT_FILE_ADDED:
				file = os.path.join(data.folder,data.name)
				print("New file: %s" % file)
				#self.download_file(fn)
		
			#try to grab another event
			typ,data = camera.wait_for_event(1)

def change_man_cfg(iso, aperture, shutterspeed):
	'''
	wrapper function to help with managing manual photo config
	'''
	print("changing config to: iso: " + iso + ", aperture: " + aperture + ", shutterspeed: " + shutterspeed)
	change_cfg('iso',iso)
	change_cfg('aperture', aperture)
	change_cfg('shutterspeed', shutterspeed)
	return(0)	
			
def take_darks():
	'''
	Take darks for calibrating the iso
	'''
	print("Taking dark frames")
	change_man_cfg('6400', '3.5', '1/8000')
	takeShot("darks/", 20)

def take_bias():
	'''
	Calibrate the noise by taking bias frames
	'''
	print("Taking bias frames")
	change_man_cfg('6400', '3.5', '1')
	takeShot("bias/", 20)
	
def take_lights():
	'''
	Calibrate the color by taking shots of even light
	'''
	print("Taking light frames")
	input("Put paper in front of your camera and put your phone in the white background, or do it in the sun\npress enter once done")
	change_man_cfg('6400', '3.5', '1/80')
	takeShot("light/",20)
	
camera.exit()
print('SUCCESS!!!')
