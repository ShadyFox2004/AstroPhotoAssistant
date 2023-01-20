import os

import modules.camera as cam
#import modules.presiril as srl

answer = input("Is the flats, darks and biases taken?(Y/N): ")
if answer == 'N' or answer == 'n':
    print("starting calibration")
    cam.take_darks()
    cam.take_biases()
    cam.take_flats()
else:
    print("skipping calibration")

answer = input("skipping lights?(Y/N): ")
if answer == 'N' or answer == 'n':
    print('Taking light frames')
    cam.take_lights()


cam.camera.exit()
