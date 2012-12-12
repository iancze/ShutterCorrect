#ShutterCorrect

For the most up to date information about using ShutterCorrect, visit the wiki at https://github.com/iancze/ShutterCorrect/wiki 


* Ian Czekala
* Email: iczekala@cfa.harvard.edu
* Organization: Harvard-Smithsonian Center for Astrophysics

Calculate a shutter correction map for digital images. Primarily designed for correcting astronomical images to achieve the desired illumination.

## Usage 

It only makes sense to apply the shutter correction to the flat field images and science frames, since it corrects for the illumination pattern of the CCD chip. Do not use shutterCorrect on bias or dark frames. That said, before using shutterCorrect, make sure your flat field and science frames have been bias and dark corrected (but not flat field corrected).

General help:

	python shutterCorrect.py -h


	usage: shutterCorrect.py [-h] [-f FILENAME [FILENAME ...]] [-l LISTNAME]
                         [--exptime_kw EXPTIME_KW] [--binning BINNING]
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
	  --binning BINNING     "2x2" or "1x1." Assumes image is square. Default is
				"2x2"
	  --prefix PREFIX       string or character to prepend to processed filenames.
				Default is "s"

		usage: fit_pdfs.py [-h] [-f FILENAME [FILENAME ...]] [-l LISTNAME]
				   [--exptime_kw EXPTIME_KW] [--binning BINNING]
				   [--prefix PREFIX]

## Examples

Correct a single image, my_file.fits

	python shutterCorrect.py --filename my_file.fits

If the header keyword has an exposure_time keyword other than `EXPTIME`, such as EXP
	
	python shutterCorrect.py --exptime_kw EXP --filename my_file.fits

###If you have multiple files that need correcting

Option 1:

	python shutterCorrect.py --filename file1.fits file2.fits file3.fits

Option 2: Create a file that holds a list of all of the files, for example

	ls *.fits > my_list.list

Use `shutterCorrect.py` in batch mode

	python shutterCorrect.py --listname my_list.list
	

