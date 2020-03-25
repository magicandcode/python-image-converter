"""Convert images in source directory and save into target directory.

Args:
    source - Dir with images to convert.
    target -
        Dir in which to save converted images.
         (default: source_directory)
Usage:
    python3 -m image_converter <source> <[,target]>
"""

import sys
from pathlib import Path
from typing import Sequence

from PIL import Image


def main(directories: Sequence[str]) -> None:
    try:
        # Use source as target if target is omitted.
        if len(directories) == 1:
            directories = directories[0], directories[0]
        SOURCE_DIRECTORY, TARGET_DIRECTORY = directories
    except (AttributeError, IndexError, TypeError, ValueError) as e:
        raise e
    else:
        converter: ImageConverter = ImageConverter(SOURCE_DIRECTORY,
                                                   TARGET_DIRECTORY)
        converter.convert_images()


class ImageConverter:
    """Image converter able to bulk convert images from one format to
     another. Works with both relative and absolute directory paths.
    Uses the Pillow library and the pathlib module to handle images and
     paths.
    """

    FROM_FORMAT, TO_FORMAT = 'jpg', 'png'
    _directories = []
    _version = 1.0

    def __init__(self, source_dir, target_dir=None):
        """Set directories and print program header."""
        self.directories = source_dir, target_dir
        self._get_header()

    @property
    def directories(self):
        """Return source and target directories as tuple."""
        return self._directories

    @property
    def source_dir(self):
        """Return source directory as pathlib.Path object."""
        return Path(str(self.directories[0]))

    @property
    def target_dir(self):
        """Return target directory as pathlib.Path object."""
        return Path(str(self.directories[1]))

    @directories.setter
    def directories(self, dirs):
        """Set source and target directories as tuple.

        Use source as target directory if target directory is omitted.

        Arguments:
            dirs -- source and target directory in ordered container
        Exceptions:
            AttributeError, TypeError, ValueError
        """
        try:
            if dirs[1] is None:
                dirs = dirs[0], dirs[0]  # Use source as target
            source_dir, target_dir = (str(directory) for directory in dirs)
        except (AttributeError, TypeError, ValueError) as e:
            print('Unable to set directories, see error message:',
                  str(e).capitalize())
        else:
            self._directories = source_dir, target_dir

    @property
    def _source_images(self):
        """Get all cls.FROM_FORMAT images in the source directory as a
        generator to enable iteration over the source images.
        Only meant for testing and private use.
        """
        return self.source_dir.glob(f'*.{self.FROM_FORMAT}')

    def _create_target_dir(self):
        """Create target directory if it doesn't exist.
        Return boolean to indicate success or failure.
        If the directory exists, True is returned. Only return False if
        there is an exception other than FileExistsError.
        """
        try:
            if self.source_dir != self.target_dir:
                self.source_dir.parent.joinpath(
                    self.target_dir.joinpath()).mkdir()
            return True
        except FileExistsError:
            return True  # File already exists
        except (ValueError, TypeError, AttributeError) as e:
            print(str(e).capitalize())
            return False

    def _convert_image(self, source_img):
        to_format = self.TO_FORMAT
        with Image.open(source_img.joinpath()) as img:
            img.save(
                self.target_dir.joinpath(f'{source_img.stem}.{to_format}'),
                to_format)

    # Todo: Refactor!
    # Todo: Enable override of cls.TO_FORMAT via parameter to_format
    def convert_images(self):
        """Convert FROM_FORMAT images in source directory to TO_FORMAT
        images and save in the target directory.
        """
        # Todo: Return bool or exception to be caught?
        if not self._create_target_dir():
            print('Unable to create target directory '
                  f'{self.target_dir.joinpath()}. Conversion process aborted.')
            return False

        try:
            conversions = 0  # Number of converted images
            iterations = 0  # Number of source images iterated over

            for iterations, source_img in enumerate(self._source_images):
                try:
                    iterations += 1  # Add 1 to count the first image
                    target_img_name = f'{source_img.stem}.{self.TO_FORMAT}'
                except (AttributeError, ValueError, TypeError) as e:
                    print(str(e).capitalize())
                    # Something unexpected went wrong and we don't know
                    # how to handle it; Return to abort the conversion.
                    return False
                try:
                    # Open target image to check if it exists.
                    print(f'Attempting to open image {target_img_name} in '
                          f'{self.target_dir.joinpath()}...')
                    with Image.open(
                            self.target_dir.joinpath(target_img_name)) as _:
                        # Only attempt to open image to see if it exists
                        pass
                except FileNotFoundError:
                    print('The image does not exist, initiating conversion'
                          '...')
                    print(f'Converting image to {self.TO_FORMAT}...')
                    self._convert_image(source_img)
                    print(f'Successfully saved {target_img_name} to '
                          f'{self.target_dir.joinpath()}', end='\n\n')
                    conversions += 1
                    continue
                except Exception as e:  # Todo: Specify exceptions
                    print(str(e).capitalize())
                    # Something unexpected went wrong and we don't know
                    # how to handle it; Return to abort the conversion.
                    return False
                else:
                    print(f'Image {target_img_name} already exists in '
                          f'{self.target_dir.joinpath()}.', end='\n\n')
                    continue  # Image already exist in target directory
            if iterations > 0:
                images_n_string = 'images' if iterations > 1 else 'image'
                print(f'Converted {conversions} of {iterations} '
                      f'{self.FROM_FORMAT.upper()} {images_n_string} to '
                      f'{self.TO_FORMAT.upper()}', end='\n\n')
                return True  # Successfully converted at least 1 image
            raise ValueError(f'Could not find any {self.FROM_FORMAT.upper()} '
                             'images in source folder '
                             f'{self.source_dir.joinpath()}.')
        except (ValueError, TypeError, AttributeError) as e:
            print('Unable to process conversion: ')
            print(str(e).capitalize())
            return False

    def _get_header(self):
        """Print program header with setup info."""
        border = '*'*45
        print('', border, f' Image Converter v. {self._version}',
              ' A project for Z2M Python by @magicandcode', border,
              f'Source folder: {self.source_dir.joinpath()} '
              f'[converting from {self.FROM_FORMAT.upper()}]',
              f'Target folder: {self.target_dir.joinpath()} '
              f'[converting to {self.TO_FORMAT.upper()}]', sep='\n', end='\n\n')


if __name__ == '__main__':
    try:
        # Todo: Ask for input if no commandline arguments are given.
        # Get directories from command line arguments.
        directories = sys.argv[1:3]
        main(directories)
    except (AttributeError, IndexError, TypeError, ValueError) as e:
            print('Unable to set source and target directory, please try '
                  'again; ')
            print(str(e).capitalize())
