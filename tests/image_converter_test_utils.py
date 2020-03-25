"""Util module for test.test_image_converter"""
import shutil
from pathlib import Path


# Default tests values for source and target directories when running
#  tests. Absolute paths are also possible but it is recommended to
# keep to these preset values when testing.
SOURCE, TARGET = 'pokedex', 'pokedex_png'
CONVERTED_IMAGES = []


# Todo: Track converted images to only remove these after tests.
def set_up():
    """Remove target directory before running tests. If target is the same as
    the source, the user is prompted to delete the generated files manually.
    The target file will only be removed if
    """
    if SOURCE == TARGET:
        print('Remove the converted files manually, the source directory will '
              'not be removed...')
        return False
    try:
        print('Removing target directory before tests...')
        Path(TARGET).rmdir()
        return True
    except FileNotFoundError:
        print('Target directory does not exists, continues with testing...')
        return True  # Everything is already set up to run the tests
    except OSError:
        # Directory exists and is not empty
        print(
            'Target directory exists and is not empty, removing directory and '
            'all of its content...')
        shutil.rmtree(TARGET)  # Remove directory and its content


def tear_down():
    """Tear down function to run after tests. Prints message to prompt
     user to remove generated images in the source directory manually.
    """
    print('Tests are run. Generated directories/images will not be'
          'removed until next test is run. Remove generated images in'
          'the source directory manually before running next test.')
    return True

