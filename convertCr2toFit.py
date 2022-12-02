from astropy.nddata import Cutout2D, CCDData
import numpy as np
import matplotlib.pyplot as plt
import rawpy
from astropy.io import fits

import os

path = "/home/shadyfox/BigData2/JUPYTER_EXPLORATION/LIGHTS/Jupyter/"
images = []

for x in os.listdir(path):
    if x.endswith(".CR2"):
        # Prints only text file present in My Folder
        print(x)
        images.append(rawpy.imread(path+x))

hdulist = fits.HDUList([])

hdulist.append(fits.PrimaryHDU(images[0].raw_image))

for i in images:
    ccd = CCDData(i.raw_image,meta={'object':'jupyter'},unit='adu')
    hdu = fits.ImageHDU(ccd)
    hdulist.append(hdu) # add file 

hdulist.info()
hdulist.writeto("jupyter.fit")
