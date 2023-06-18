# Author: Matteo Del Grosso
# Date: 18.6.2023
#
# Problem/Motivation:
#   When migrating all image metadata from Capture One Pro to Lightroom Classic (LrC), the following problem has occurred:
#   Lightroom Classic does not update the metadata of an image if the xmp metadata file is "older" than the corresponding image file.
#
# Solution:
#   Find all image files in the photo archive and update the timestamp of the associated xmp metadata file to the current date/time.
#   This will ensure that the metadata xmp file has a later modified date/time than the associated image file, thus Lightroom Classic
#   will read and update the metadata from the xmp file. The update may occur automatically by LrC or when the corresponding command is given.
#
# Procedure:
#   Iterate over all image files in photo archive and identify different types of images files and their associate xmp metadata xmp-file
#
# Image file types (file extensions) considered (case of extension is not relevant):
#   NEF - Nikon RAW files
#   DNG - Digital Negative RAW files
#   RW2 - Panasonic Lumix RAW files
#   RAF - Fujifilm RAW files
#   JPG - JPEG files

from collections import Counter
import os
from pathlib import Path


photo_root_folder: Path = Path("e:/photo")
# image_file_types = ("dng", "nef", "raf", "rw2", "jpg")

image_type_counter = Counter(dng=0, nef=0, raf=0, rw2=0, jpg=0)


def main():
    total_image_count_with_xmp: int = 0
    total_image_count_without_xmp: int = 0
    total_file_count: int = 0
    for dir_path, dir_names, files in os.walk(photo_root_folder):
        total_file_count += len(files)
        print(f"{dir_path}: {total_file_count} files")
        for file in files:
            file_type: str = Path(file).suffix.lower()[1:]
            if file_type in image_type_counter.keys():
                image_type_counter[file_type] += 1
                # print(f"Image file: {file}")
                image_xmp_file: Path = Path(dir_path) / Path(file).with_suffix(".xmp")
                if image_xmp_file.exists():
                    # print(f"Metadata file {image_xmp_file} not found for: {file}")
                    total_image_count_with_xmp += 1
                else:
                    total_image_count_without_xmp += 1

    print(f"Total number of images: {image_type_counter.total()}")
    print(f"Total images with xmp files: {total_image_count_with_xmp}")
    print(f"Total images without xmp files: {total_image_count_without_xmp}")
    assert (
        total_image_count_with_xmp + total_image_count_without_xmp
        == image_type_counter.total()
    ), "Image count error"
    print(f"Total files: {total_file_count}")

    for image_type, count in image_type_counter.items():
        print(f"{image_type}: {count}")


if __name__ == "__main__":
    main()
