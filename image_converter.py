import sys
from pathlib import Path

from PIL import Image


class ImageConverter(object):
    FROM_FORMAT, TO_FORMAT = 'jpg', 'png'
    _directories = []
    _source_images: None
    _version = 1.0

    def __init__(self, source_dir, target_dir=None):
        self.directories = source_dir, target_dir
        self._get_header()  # Init header before conversion request

    @property
    def directories(self):
        return self._directories

    @property
    def source_dir(self):
        return Path(str(self.directories[0]))

    @property
    def target_dir(self):
        return Path(str(self.directories[1]))

    @directories.setter
    def directories(self, dirs):
        try:
            if dirs[1] is None:
                dirs = dirs[0], dirs[0]  # Use source as target
            source_dir, target_dir = (str(directory) for directory in dirs)
        except (AttributeError, TypeError, ValueError) as e:
            print('Unable to set directories, see error message:',
                  str(e).capitalize())
        else:
            self._directories = source_dir, target_dir

    def _get_source_images(self):
        source_dir = Path(self.source_dir)
        return source_dir.glob(f'*.{self.FROM_FORMAT}')

    @property
    def source_images(self):
        return self._get_source_images()

    def _create_target_dir(self):
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

    def _convert_images_to_source(self):
        pass

    def convert_images(self, to_format=None):
        to_format = self.TO_FORMAT if to_format is None else to_format
        target_dir_exists = self._create_target_dir()

        if not target_dir_exists:
            print('Unable to create target directory '
                  f'{self.target_dir.joinpath()}. Conversion process aborted.')
            return False

        try:
            converted = 0
            i = 0
            for i, source_img in enumerate(self.source_images):
                try:
                    i += 1  # Add one to count first image
                    target_img_name = f'{source_img.stem}.{to_format}'
                except (AttributeError, ValueError, TypeError) as e:
                    print(str(e).capitalize())
                    return False
                try:
                    # Try to open image in target dir to see if it exists
                    print(f'Attempting to open image {target_img_name} in '
                          f'{self.target_dir.joinpath()}...')
                    with Image.open(self.target_dir.joinpath(
                            target_img_name)) as _:
                        # Only attempt to open image to see if it exists
                        pass
                except FileNotFoundError:
                    print(
                        'The image does not exist, initiating conversion'
                        '...')
                    print(f'Converting image to {self.TO_FORMAT}...')
                    with Image.open(source_img.joinpath()) as img:
                        img.save(self.target_dir.joinpath(
                            f'{source_img.stem}.{to_format}'), to_format)
                        print(f'Successfully saved {target_img_name} to '
                              f'{self.target_dir.joinpath()}', end='\n\n')
                        conversions += 1
                    continue
                except Exception as e:
                    print(str(e).capitalize())  # Something went wrong...
                    return False
                else:
                    print(f'Image {target_img_name} already exists in '
                          f'{self.target_dir.joinpath()}.')
                    continue  # Image already exist in target directory
            if i > 0:
                images_n_string = 'images' if i > 1 else 'image'
                print(f'Converted {converted} of {i} {self.FROM_FORMAT.upper()}'
                      f' {images_n_string} to {self.TO_FORMAT.upper()}',
                      end='\n\n')
                return True  # Successfully converted at least 1 image
            raise ValueError(f'Could not find any {self.FROM_FORMAT.upper()} '
                             'images in source folder '
                             f'{self.source_dir.joinpath()}.')
        except (ValueError, TypeError, AttributeError) as e:
            print('Unable to process conversion: ')
            print(str(e).capitalize())

    def _get_header(self):
        border = '*' * 45
        print('',
              border,
              f' Image Converter v. {self._version}',
              ' A project for Z2M Python by @magicandcode', border,
              f'Source folder: {self.source_dir.joinpath()} '
              f'[converting from {self.FROM_FORMAT.upper()}]',
              f'Target folder: {self.target_dir.joinpath()} '
              f'[converting to {self.TO_FORMAT.upper()}]', sep='\n', end='\n\n')

    def _count_source_images(self):
        return len(list(self.source_images))


if __name__ == '__main__':
    # Get argv directories
    print('get the dirs!')
    try:
        dirs = sys.argv[1:3]
        print('dirs: ', dirs)
        if len(dirs) == 1:  # Use source as target if target is missing
            dirs = dirs[0], dirs[0]
        dirs = (str(directory) for directory in dirs)
    except Exception as e:
        print('Unable to set source and target directory, please try again: ')
        print(str(e).capitalize())
    else:
        converter = ImageConverter(*dirs)
        converter.convert_images()
