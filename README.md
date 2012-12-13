#ShutterCorrect



* Ian Czekala
* Email: iczekala@cfa.harvard.edu
* Organization: Harvard-Smithsonian Center for Astrophysics

This project contains two scripts. The first, `createMap.py`, is to create the `shutter.fits` file from a set of dome or twilight flats. This only needs to be done once, and if you are using this code for the MMTCam, it has already been done for you. For detailed information on this process, visit the wiki: https://github.com/iancze/ShutterCorrect/wiki 

The second script, 'shutterCorrect.py`, is used to correct flat and science frames for shutter travel time. Its usage is detailed below.

For CfA machines, Tom Aldcroft has built a full-featured Python 2.7 installation, which you can use this by updating your PATH as follows. This code will not work on the default Python installation by the CF (version 2.4), because it is painfully out of date:

For csh or tcsh:

	set path=(/data/astropy/ska/arch/x86_64-linux_CentOS-5/bin $path)

For bash:

	export PATH="/data/astropy/ska/arch/x86_64-linux_CentOS-5/bin:$PATH"

## Usage 

It only makes sense to apply the shutter correction to the flat field images and science frames, since it corrects for the illumination pattern of the CCD chip. Do not use shutterCorrect on bias or dark frames. That said, before using shutterCorrect, make sure your flat field and science frames have been bias and dark corrected (but not flat field corrected), and are trimmed to the same size as the `shutter.fits` file (in this case, 1024 x 1024 pixels). 

General help:

	python shutterCorrect.py -h

	usage: shutterCorrect.py [-h] [-f FILENAME [FILENAME ...]] [-l LISTNAME]
				 [--exptime_kw EXPTIME_KW] [--binning {1x1,2x2}]
				 [--prefix PREFIX]

	Correct CCD images (flats and science frames) for shutter timing effects.

	optional arguments:
	  -h, --help            show this help message and exit
	  -f FILENAME [FILENAME ...], --filename FILENAME [FILENAME ...]
				Filename or filenames separated by whitespace to
				shutter correct.
	  -l LISTNAME, --listname LISTNAME
				listname to file containing files to process (one on
				each line).
	  --exptime_kw EXPTIME_KW
				header keyword for the exposure time, default is
				"EXPTIME"
	  --binning {1x1,2x2}   "2x2" or "1x1." Assumes image is square. Default is
				"2x2"
	  --prefix PREFIX       string or character to prepend to processed filenames.
				Default is "s"


## Examples

Correct a single image, my_file.fits

	python shutterCorrect.py --filename my_file.fits

If the header keyword has an exposure_time keyword other than `EXPTIME`, such as EXP
	
	python shutterCorrect.py --exptime_kw EXP --filename my_file.fits

*not implemented yet* If your frames are `1x1` binning, instead of the `2x2` binning default

	python shutterCorrect.py --binning 1x1 --filename my_file.fits

###If you have multiple files that need correcting

Option 1:

	python shutterCorrect.py --filename file1.fits file2.fits file3.fits

Option 2: Create a file that holds a list of all of the files, for example

	ls *.fits > my_list.list

then use `shutterCorrect.py` in batch mode

	python shutterCorrect.py --listname my_list.list
	

