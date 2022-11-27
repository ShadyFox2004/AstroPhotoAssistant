import modules.camera as cam
import modules.presiril as srl

cam.take_darks()
cam.take_biases()
cam.take_flats()

srl.process(".")
