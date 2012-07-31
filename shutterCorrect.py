import pyfits
import numpy as np

'''
shutterCorrect.py
Ian Czekala
Email: iczekala@cfa.harvard.edu
Project Website: https://github.com/iancze/ShutterCorrect/wiki

Input: Give shutter correct well exposed and stacked twilight flats at different lengths of exposure. Frames should have already been subjected to standard processing, bias subtraction, overscan correction, and dark current correction. In addition, it will help the statistics if many frames are averegade togethere to reduce the noise. Assume that all frames are the same shape and dimensions.

Suggested exposure times:
These may vary based upon how long your shutter travel time will take, but assuming a shutter travel time of 0.010 seconds, some exposures of 0.1, 1.0, 5.0, 10.0 and 60 seconds or longer will be helpful. Make the longest exposure as long as is practically possible, since for this frame it is assumed that the shutter correction is negligable. 

ShutterCorrect will then deliver a 2D fits frame that is a map of the amount of time (in seconds) that each pixel is missing in the exposure due to the shutter travelling, called the "shutter map," or $t_{\rm shutter}$. The commanded exposure time is labelled as $t_{\rm exp}$.

Assuming that the central pixels of the frame achieved 100% illumination, you can use the shutter map to determine the illumination map, which shows that the illumination percentage that the rest of the frame achieved::

    illumination map = (Amount of time exposed)/(Amount of time commanded to expose)
    = $\frac{t_{\rm exp} - t_{\rm shutter}}{t_{\rm exp}}$

One can use the shutter map to correct any given frame to a uniform illumination. This is desireable for any flat field images or science images taken during an astronomical observing session, called "user frame." The corrected frame will be::

    corrected frame = \frac{user frame}{illumination map} = \frac{user frame \times t_{\exp}}{t_{\rm exp} - t_{\rm shutter}}


From the shutter map it is also possible to infer the shutter travel time. Essentially, the central pixels should be approximately 0.0 seconds, while the edge pixels will read a value approximately the total amount of time it takes the shutter to open and close.
'''

class Exposure(object):
    '''The exposure object for a given nominal time'''
    def __init__(self,exptime,raw_fname):
        self.exptime = exptime #nominal exposure time (s)
        self.raw_fname = raw_fname #filename for raw flat
        self.raw_data = openData(self.raw_fname) #open the raw frame
        self.max_val = self.calc_central() #compute the max value for raw frame
        self.norm = self.calc_norm() #calculate the normalized frame

    def calc_central(self,percentage=0.05):
        '''Determine the central "maximum" value of the exposure in each frame, which will be used to normalize the image to. Default value is the central 5%'''
        rows,columns = self.raw_data.shape
        row_span = rows * percentage
        row_min = int((rows - row_span)/2)
        row_max = int((rows + row_span)/2)
        col_span = columns * percentage
        col_min = int((columns - col_span)/2)
        col_max = int((columns + col_span)/2)
        #print(row_min,row_max,col_min,col_max)
        max_val = np.median(self.raw_data[row_min:row_max,col_min:col_max])
        #print(max_val)
        return max_val

    def calc_norm(self):
        '''Normalize the raw data by the max value, so that the maximum value in the normed image is approximately 1.0'''
        return self.raw_data/self.max_val

    def create_illumination(self,master_exposure):
        self.master_exposure = master_exposure
        self.illumination = self.norm/self.master_exposure.norm

    def create_shutter(self):
        self.shutter = self.exptime * (1.0  - self.illumination)

    def writeFrames(self):
        writeFrame(self.norm,"Frames/%snorm.fits" % self.exptime)
        writeFrame(self.illumination,"Frames/%sillumination.fits" % self.exptime)
        writeFrame(self.shutter,"Frames/%sshutter.fits" % self.exptime)

def openData(filename):
    hdulist = pyfits.open(filename)
    data = hdulist[0].data
    hdulist.close()
    return data

def writeFrame(data,filepath):
    hdu = pyfits.PrimaryHDU(data)
    hdulist = pyfits.HDUList(hdu)
    hdulist.writeto(filepath)

def create_master_shutter(exposure_list):
    #Inversely weight these by the noise.
    pass

def main():
    # Fill out the following values with your frames. Will write frames into a Frames/ subdirectory.

    # Each item in the dictionary is keyed by the exposure time. For example
    #{exptime1: filename1, exptime2: filename2}
    frame_dictionary = {0.1:"Frames/0p1.fits",1:"Frames/1.fits",120:"Frames/120.fits"}

    #Dictionary of exposure objects
    exposure_dictionary = {}
    for exptime in frame_dictionary.keys():
        exposure_dictionary[exptime] = Exposure(exptime,frame_dictionary[exptime])

    #Set the longest exposure where the shutter correction is assumed to be negligable.
    max_exp = max(list(exposure_dictionary.keys()))
    long_exp = exposure_dictionary[max_exp]
    #Create the illumination and shutter maps for each exposure. Ideally, all of the shutter maps should be the same, but in reality, they will differ due to noise, since there will be the most signal to noise in the shortest exposures.     
    for exposure in exposure_dictionary.values():
        exposure.create_illumination(long_exp)
        exposure.create_shutter()
        exposure.writeFrames()

    #Inspect all of the frames, but then we can create a master frame by averageing together the best shutter maps. The shutter map for the longest exposure should be 0.0, since we defined this to have approximately zero shutter correction.
    #create_master_shutter()

if __name__=="__main__":
    main()
