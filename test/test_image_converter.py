import shutil

import pytest
from pathlib import Path

from image_converter import ImageConverter


SOURCE, TARGET = 'pokedex', 'new_pokedex'


def set_up():
    """Remove target directory before running tests. If target is the same as
    the source, the user is prompted to delete the generated files manually.
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


set_up()


@pytest.fixture
def converter():
    return ImageConverter(SOURCE, TARGET)


@pytest.fixture
def src_converter():
    return ImageConverter(SOURCE)


def test_can_get_target_and_source_dirs(converter):
    expected = SOURCE, TARGET
    assert converter.directories == expected


def test_can_use_source_dir_as_target(src_converter):
    expected = SOURCE, SOURCE
    assert src_converter.directories == expected


def test_can_get_files_of_format_from_source(converter):
    got = len(list(converter._source_images))
    expected = 4
    assert got is expected


def test_cannot_set_source_images(converter):
    with pytest.raises(AttributeError):
        converter._source_images = []


def test_can_create_target_dir(converter):
    target_dir_is_created = converter._create_target_dir()
    assert target_dir_is_created is True
    assert converter.target_dir.exists() is True


def test_can_convert_images_and_save_into_target_dir_if_target(converter):
    converter.convert_images()
    assert len(list(
        converter.target_dir.glob(f'*.{ImageConverter.TO_FORMAT}')
    )) is 4


def test_can_convert_images_and_save_into_target_dir_if_source(src_converter):
    src_converter.convert_images()
    assert len(list(
        src_converter.target_dir.glob(f'*.{ImageConverter.TO_FORMAT}')
    )) is 4
