
import argparse
import pyfits
import sys

'''
shutterCorrect.py
Ian Czekala
Email: iczekala@cfa.harvard.edu
Project Website: https://github.com/iancze/ShutterCorrect/wiki
'''

#If using a different version of the shutter map, change this file."
shutter_map = pyfits.open("shutter.fits")[0].data

def correct_image(filename, exptime_kw, binning, prefix):
    hdulist = pyfits.open(filename)
    data = hdulist[0].data
    header = hdulist[0].header
    exptime = header[exptime_kw]

    corrected = data / (1.0 - shutter_map/exptime) 

    hdulist[0].data = corrected
    header.update('SHUTCOR', 'TRUE')
    hdulist.writeto(prefix + filename)
    hdulist.close()

def main():
    parser = argparse.ArgumentParser(prog='shutterCorrect.py', description='Correct CCD images (flats and science frames) for shutter timing effects.')
    parser.add_argument('-f','--filename',nargs='+',help='Filename or filenames separated by whitespace to shutter correct.')
    parser.add_argument('-l','--listname',help='listname to file containing files to process (one on each line).')
    parser.add_argument('--exptime_kw',help='header keyword for the exposure time, default is "EXPTIME"',default='EXPTIME')
    parser.add_argument('--binning',help='"2x2" or "1x1." Assumes image is square. Default is "2x2"',default='2x2',choices=('1x1','2x2'))
    parser.add_argument('--prefix',help='string or character to prepend to processed filenames. Default is "s"',default='s')

    if 'python' in sys.argv[0]:
        offset = 2
    else:
        offset = 1
    args = parser.parse_args(sys.argv[offset:])

    if args.binning == "1x1":
        raise NotImplementedError("1x1 binning option not yet implemented.")

    if args.listname != None:
        filelist = [i.rstrip() for i in open(args.listname).readlines()]
    else: filelist = args.filename
    for filename in filelist:
        correct_image(filename, args.exptime_kw, args.binning, args.prefix)

if __name__=="__main__":
    main()
