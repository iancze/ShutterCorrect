import pyfits
import numpy as np

'''
ShutterCorrect



'''

##Normalize each frame to the max number of counts in the image, which is found by taking an average of the central thousand pixels in a 100x100 box centered on [978:1078,979:1079], since this was trimmed in the X (column) direction.

#[978:1078,979:1079]
#0p1.fits
# NPIX      MEAN    STDDEV       MIN       MAX     MIDPT
# 10161     5634.     32.21     5537.     5730.     5632.

#1.fits
# NPIX      MEAN    STDDEV       MIN       MAX     MIDPT
# 10201    43566.     605.8    41824.    44920.    43667.

#120.fits
# NPIX      MEAN    STDDEV       MIN       MAX     MIDPT
# 10169    42404.      383.    41274.    43554.    42376.




def openRaw():
    '''Open the raw frames'''
    global data0p1,data1,data120
    hdulist0p1 = pyfits.open("Frames/0p1.fits")
    data0p1 = hdulist0p1[0].data
    hdulist1 = pyfits.open("Frames/1.fits")
    data1 = hdulist1[0].data
    hdulist120 = pyfits.open("Frames/120.fits")
    data120 = hdulist120[0].data

#Here put routine to determine the central illumination value (using image size, boxing percentage, etc).

def openData(filename):
    hdulist = pyfits.open(filename)
    data = hdulist[0].data
    return data

def writeFrame(data,filepath):
    hdu = pyfits.PrimaryHDU(data)
    hdulist = pyfits.HDUList(hdu)
    hdulist.writeto(filepath)

def writeNormed():
    '''Create and write the normalized frames'''
    norm0p1 = data0p1/5634.0
    norm1 = data1/43566.0
    norm120 = data120/42404.0

    #Write normalized frames
    hdu_norm0p1 = pyfits.HDUList(pyfits.PrimaryHDU(norm0p1))
    hdu_norm0p1.writeto("Frames/norm0p1.fits")
    hdu_norm1 = pyfits.HDUList(pyfits.PrimaryHDU(norm1))
    hdu_norm1.writeto("Frames/norm1.fits")
    hdu_norm120 = pyfits.HDUList(pyfits.PrimaryHDU(norm120))
    hdu_norm120.writeto("Frames/norm120.fits")

def loadNormed():
    global norm0p1,norm1,norm120
    hdulist0p1 = pyfits.open("Frames/norm0p1.fits")
    norm0p1 = hdulist0p1[0].data
    hdulist1 = pyfits.open("Frames/norm1.fits")
    norm1 = hdulist1[0].data
    hdulist120 = pyfits.open("Frames/norm120.fits")
    norm120 = hdulist120[0].data

def make_correction():
    global cor0p1,cor1,cor120
    cor0p1 = norm0p1/norm120
    cor1 = norm1/norm120
    cor120 = norm120/norm120
    #Write correction frames
    hdu_cor0p1 = pyfits.HDUList(pyfits.PrimaryHDU(cor0p1))
    hdu_cor0p1.writeto("Frames/cor0p1.fits")
    hdu_cor1 = pyfits.HDUList(pyfits.PrimaryHDU(cor1))
    hdu_cor1.writeto("Frames/cor1.fits")
    hdu_cor120 = pyfits.HDUList(pyfits.PrimaryHDU(cor120))
    hdu_cor120.writeto("Frames/cor120.fits")

def loadCor():
    global cor0p1,cor1,cor120
    cor0p1 = pyfits.open("Frames/cor0p1.fits")
    cor0p1 = cor0p1[0].data
    cor1 = pyfits.open("Frames/cor1.fits")
    cor1 = cor1[0].data
    cor120 = pyfits.open("Frames/cor120.fits")
    cor120 = cor120[0].data

def calc_tshutter(illum_frame, exptime):
    t_shutter = exptime * ( 1.0 - illum_frame)
    return t_shutter

def main():
    #loadCor()
    #writeFrame(calc_tshutter(cor0p1,0.1),"Frames/t_shutter_0p1.fits")
    #writeFrame(calc_tshutter(cor1,1.0),"Frames/t_shutter_1.fits")
    shutter_0p1 = openData("Frames/t_shutter_0p1.fits")
    shutter_1 = openData("Frames/t_shutter_1.fits")
    div = shutter_0p1 / shutter_1
    sub = shutter_0p1 - shutter_1
    writeFrame(div,"Frames/t_shutter_div.fits")
    writeFrame(sub,"Frames/t_shutter_sub.fits")

if __name__=="__main__":
    main()
