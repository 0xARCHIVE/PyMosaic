# PyMosaic

A simple mosaic generating program

## Requirements

* Python3

* Pillow

## Usage

Run pymosaic.py

When prompted, either (a) type in the location of the image, or (b) drag and drop the file itself, that you want to be turned into a mosaic

Hit enter

## Large input files

If your inputted file is large then it could take a long time to generate a mosaic. You can reduce the size of the final mosaic (and thus speed up the process) by increasing the value of *size_mod* in pymosaic.py (default value of 1); the final image will then be scaled by a factor of 1/size_mod

## Output files

Three .png files are generated:

*mosaic_raw.png* - the raw (full size) mosaic. This file can be incredibly large!

*mosaic.png* - a more reasonably sized image, 1/4 of the size of the raw output in each direction

*mosaic_thumb.png* - a thumbnail of the mosaic