# Python Image Converter
Python 3 image converter built with the [Pillow library](https://pillow.readthedocs.io/en/stable/) to easily bulk convert JPG images to PNG.
Converted images can be stored in the `source directory` or a `target directory` which is created if it doesn't already exist.

This project is based on an exercise in the [Complete Python Developer:Zero to Mastery course](https://www.udemy.com/course/complete-python-developer-zero-to-mastery/?referralCode=D505BF7D33948CF0CC48).

### Installation
Install all dependencies, preferably in a new virtual environment.
```
pip install -r requirements.txt
```
Now you can use the `image_converter` module either as an import or run it from the command line.

### Use the Image Converter
The image converter takes two arguments: `source directory` and `target directory`.
Target directory is optional. The program will save the converted files in the source directory if target directory is omitted.
Both relative and absolute paths can be used.

```
cd <root of source> # If you are using a realtive source path
python3 -m image_converter <source> <[,target]>
```
```
*********************************************
 Image Converter v. 1.0
 A project for Z2M Python by @magicandcode
*********************************************
Source folder: pokedex [converting from JPG]
Target folder: pokedex2 [converting to PNG]
images-converter

Attempting to open image  bulbasaur.png
The image does not exist, initiating conversion...
Converting image to png...
Successfully saved bulbasaur.png to pokedex2

Attempting to open image  pikachu.png
The image does not exist, initiating conversion...
Converting image to png...
Successfully saved pikachu.png to pokedex2

Attempting to open image  squirtle.png
The image does not exist, initiating conversion...
Converting image to png...
Successfully saved squirtle.png to pokedex2

Attempting to open image  charmander.png
The image does not exist, initiating conversion...
Converting image to png...
Successfully saved charmander.png to pokedex2

Converted 4 JPG images to PNG
```

If the `target directory` has a relative path and does not exist, it will be created relative to the `source directory`.

If the target directory contains PNG images with the same names as the source, these will be skipped over during conversion.
```
*********************************************
 Image Converter v. 1.0
 A project for Z2M Python by @magicandcode
*********************************************
Source folder: pokedex [converting from JPG]
Target folder: pokedex2 [converting to PNG]

Attempting to open image  bulbasaur.png
Image bulbasaur.png already exists in pokedex2ß

Attempting to open image  pikachu.png
Image pikachu.png already exists in pokedex2ß

Attempting to open image  squirtle.png
Image squirtle.png already exists in pokedex2ß

Attempting to open image  charmander.png
Image charmander.png already exists in pokedex2ß

Converted 0 of 4 JPG images to PNG
```
