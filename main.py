import time
import gphoto2 as gp
import os

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

change_cfg('iso', '6400')
change_cfg('aperture', '3.5')
change_cfg('shutterspeed', '2')
'''
def get_picture(file_name,type_of_pic, type_of_result):
    print('capturing image')
    file_path = camera.capture(type_of_pic)
    print('getting file: ' + file_path.name)
    file = camera.file_get(file_path.folder, file_path.name, type_of_result)
    print('saving it')
    file.save(str(file_name)+'.cr2')
    print(file_name + '.cr2')
    #camera.file_delete(file_path.folder, file_path.name)
    camera.exit()
    return(0)

for i in range(0,20):
    try:
        get_picture('black'+ str(i),gp.GP_CAPTURE_IMAGE, gp.GP_FILE_TYPE_NORMAL)
        time.sleep(2) 
    except:
        get_picture('black'+ str(i),gp.GP_CAPTURE_IMAGE, gp.GP_FILE_TYPE_NORMAL)
        time.sleep(2)
'''
c = camera

event_texts = {
	gp.GP_EVENT_CAPTURE_COMPLETE: "Capture Complete",
        gp.GP_EVENT_FILE_ADDED: "File Added",
	gp.GP_EVENT_FOLDER_ADDED: "Folder Added",
	gp.GP_EVENT_TIMEOUT: "Timeout",
	}

def event_text(event_type):
	if event_type in event_texts:
		return event_texts[event_type]
	return "Unknown Event"

for i in range(1,20):
	print("Capture #%1d" % i)

	i2 = c.capture(gp.GP_CAPTURE_IMAGE)

	f2 = c.file_get(i2.folder,i2.name,gp.GP_FILE_TYPE_NORMAL)
	dest2 = os.path.join("/tmp",i2.name)

	f2.save(dest2)
	print("saved to '%s'" % dest2)

	#empty the event queue
	typ,data = c.wait_for_event(200)
	while typ != gp.GP_EVENT_TIMEOUT:
		
		print("Event: %s, data: %s" % (event_text(typ),data))
		
		if typ == gp.GP_EVENT_FILE_ADDED:
			fn = os.path.join(data.folder,data.name)
			print("New file: %s" % fn)
			#self.download_file(fn)
		
		#try to grab another event
		typ,data = c.wait_for_event(1)

c.exit()
print('SUCCESS!!!')
